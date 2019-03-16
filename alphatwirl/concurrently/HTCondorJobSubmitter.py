#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import os, sys
import subprocess
import collections
import time
import textwrap
import getpass
import re
import logging

import alphatwirl
from alphatwirl.misc.removal import _removed_class_method_option

from .exec_util import try_executing_until_succeed, compose_shortened_command_for_logging

##__________________________________________________________________||
# https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=MagicNumbers
HTCONDOR_JOBSTATUS = {
    0: "Unexpanded",
    1: "Idle",
    2: "Running",
    3: "Removed",
    4: "Completed",
    5: "Held",
    6: "Transferring_Output",
    7: "Suspended"
}

##__________________________________________________________________||
## HTCondor Manual:
## 2.5 Submitting a Job
## http://research.cs.wisc.edu/htcondor/manual/v8.4/2_5Submitting_Job.html
##
## condor_submit command manual
## including complete description of submit description file
## http://research.cs.wisc.edu/htcondor/manual/v8.4/condor_submit.html#man-condor-submit

## keys should be in lower case in this dict
DEFAULT_JOB_DESC_DICT = collections.OrderedDict([
    ('executable', 'run.py'),
    ('output', 'results/$(resultdir)/stdout.$(cluster).$(process).txt'),
    ('error', 'results/$(resultdir)/stderr.$(cluster).$(process).txt'),
    ('log', 'results/$(resultdir)/log.$(cluster).$(process).txt'),
    ('arguments', '$(resultdir).p.gz'),
    ('should_transfer_files', 'YES'),
    ('when_to_transfer_output', 'ON_EXIT'),
    ('transfer_input_files', '$(resultdir).p.gz'),
    ('transfer_output_files', 'results'),
    ('universe', 'vanilla'),
    ('notification', 'Error'),
    ('getenv', 'True'),
])

##__________________________________________________________________||
class HTCondorJobSubmitter(object):
    """A dispatcher that dispatches jobs to HTCondor

    Parameters
    ----------
    job_desc_dict : dict
        A dict representing an HTCondor job description. A copy of
        `DEFAULT_JOB_DESC_DICT` that is updated with this option will
        be used as a baseline job description for job submissions.
        This option is typically used to specify requirements, e.g.,
        `{'request_memory', '250'}`

    """

    @_removed_class_method_option('job_desc_extra', msg='use job_desc_dict instead')
    def __init__(self, job_desc_dict=None):

        if job_desc_dict is None:
            job_desc_dict = dict()

        self.job_desc_dict = DEFAULT_JOB_DESC_DICT.copy()
        for k, v in job_desc_dict.items():
            self.job_desc_dict[k.lower()] = v # not using update() in case
                                              # job_desc_dict is ordered

        self.clusterprocids_outstanding = [ ]
        self.clusterprocids_finished = [ ]

    def run(self, workingArea, package_index):
        """Submit a job

        If you need to submit multiple jobs, it is usually much faster
        to use `run_multiple()` than to use this method multiple
        times.

        Parameters
        ----------
        workingArea :
            A workingArea
        package_index : int
            A package index

        Returns
        -------
        str
            The run ID of the job

        """

        return self.run_multiple(workingArea, [package_index])[0]

    def run_multiple(self, workingArea, package_indices):
        """Submit multiple jobs

        Parameters
        ----------
        workingArea :
            A workingArea
        package_indices : list(int)
            A list of package indices

        Returns
        -------
        list(str)
            The list of the run IDs of the jobs

        """

        if not package_indices:
            return [ ]

        job_desc = self._compose_job_desc(workingArea, package_indices)

        clusterprocids = submit_jobs(job_desc, cwd=workingArea.path)

        self.clusterprocids_outstanding.extend(clusterprocids)

        return clusterprocids

    def _compose_job_desc(self, workingArea, package_indices):

        job_desc_dict = self.job_desc_dict.copy()
        job_desc_dict['executable'] = workingArea.executable

        extra_input_files = sorted(list(workingArea.extra_input_files))
        if extra_input_files:
            job_desc_dict['transfer_input_files'] += ', ' + ', '.join(extra_input_files)

        job_desc = '\n'.join(['{} = {}'.format(k, v) for k, v in job_desc_dict.items()])

        package_paths = [workingArea.package_relpath(i) for i in package_indices]
        resultdir_basenames = [os.path.splitext(p)[0] for p in package_paths]
        resultdir_basenames = [os.path.splitext(n)[0] for n in resultdir_basenames]
        job_desc_queue_line = 'queue resultdir in {}'.format(', '.join(resultdir_basenames))

        job_desc = '\n'.join([job_desc, job_desc_queue_line])
        return job_desc

    def poll(self):
        """Return the run IDs of the finished jobs

        Returns
        -------
        list(str)
            The list of the run IDs of the finished jobs

        """

        clusterids = clusterprocids2clusterids(self.clusterprocids_outstanding)
        clusterprocid_status_list = query_status_for(clusterids)
        # e.g., [['1730126.0', 2], ['1730127.0', 2], ['1730129.1', 1], ['1730130.0', 1]]

        if clusterprocid_status_list:
            clusterprocids, statuses = zip(*clusterprocid_status_list)
        else:
            clusterprocids, statuses = (), ()

        clusterprocids_finished = [i for i in self.clusterprocids_outstanding if i not in clusterprocids]
        self.clusterprocids_finished.extend(clusterprocids_finished)
        self.clusterprocids_outstanding[:] = clusterprocids

        # logging
        counter = collections.Counter(statuses)
        messages = [ ]
        if counter:
            messages.append(', '.join(['{}: {}'.format(HTCONDOR_JOBSTATUS[k], counter[k]) for k in counter.keys()]))
        if self.clusterprocids_finished:
            messages.append('Finished {}'.format(len(self.clusterprocids_finished)))
        logger = logging.getLogger(__name__)
        logger.info(', '.join(messages))

        return clusterprocids_finished

    def wait(self):
        """Wait until all jobs finish and return the run IDs of the finished jobs

        Returns
        -------
        list(str)
            The list of the run IDs of the finished jobs

        """

        sleep = 5
        while True:
            if self.clusterprocids_outstanding:
                self.poll()
            if not self.clusterprocids_outstanding:
                break
            time.sleep(sleep)
        return self.clusterprocids_finished

    def failed_runids(self, runids):
        """Provide the run IDs of failed jobs


        Returns
        -------
        None

        """

        # remove failed clusterprocids from self.clusterprocids_finished
        # so that len(self.clusterprocids_finished)) becomes the number
        # of the successfully finished jobs
        for i in runids:
            try:
                self.clusterprocids_finished.remove(i)
            except ValueError:
                pass

    def terminate(self):
        """Terminate


        Returns
        -------
        None

        """

        clusterids = clusterprocids2clusterids(self.clusterprocids_outstanding)
        ids_split = split_ids(clusterids)
        statuses = [ ]
        for ids_sub in ids_split:
            procargs = ['condor_rm'] + ids_sub
            command_display = compose_shortened_command_for_logging(procargs)
            logger = logging.getLogger(__name__)
            logger.debug('execute: {}'.format(command_display))
            try:
                proc = subprocess.Popen(
                    procargs,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding='utf-8'
                )
            except TypeError:
                # no `encoding` option in Python 2
                proc = subprocess.Popen(
                    procargs,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            stdout, stderr = proc.communicate()
            logger.debug('stdout: {!r}'.format(stdout.strip()))
            logger.debug('stderr: {!r}'.format(stderr.strip()))

##__________________________________________________________________||
def clusterprocids2clusterids(clusterprocids):
    return sorted(list(set([i.split('.')[0] for i in clusterprocids])))

##__________________________________________________________________||
def submit_jobs(job_desc, cwd=None):

    procargs = ['condor_submit']
    # procargs = ['/storage/ts14043/work/cms/AlphaTwirl/20180202_condor_submit/condor_submit']

    stdout = try_executing_until_succeed(procargs, input_=job_desc, cwd=cwd)
    stdout = '\n'.join(stdout)
    # e.g., '3 job(s) submitted to cluster 3158626.'

    regex = re.compile(r"(\d+) job\(s\) submitted to cluster (\d+)", re.MULTILINE)
    match = regex.search(stdout)
    groups = match.groups()
    # e.g., ('3', '3158626')

    njobs, clusterid = groups
    njobs = int(njobs)

    change_job_priority([clusterid], 10) ## need to make configurable

    procid = ['{}'.format(i) for i in range(njobs)]
    # e.g., ['0', '1', '2', '3']

    clusterprocids = ['{}.{}'.format(clusterid, i) for i in procid]
    # e.g., ['3158626.0', '3158626.1', '3158626.2', '3158626.3']

    return clusterprocids

##__________________________________________________________________||
def query_status_for(ids, n_at_a_time=500):

    ids_split = split_ids(ids, n=n_at_a_time)
    stdout = [ ]
    for ids_sub in ids_split:
        procargs = ['condor_q'] + ids_sub + ['-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus']
        stdout.extend(try_executing_until_succeed(procargs))

    # e.g., stdout = ['688244.0 1 ', '688245.0 1 ', '688246.0 2 ']

    ret = [l.strip().split() for l in stdout]
    # e.g., [['688244.0', '1'], ['688245.0', '1'], ['688246.0', '2']]

    ret = [[e[0], int(e[1])] for e in ret]
    # a list of [clusterprocid, status]
    # e.g., [['688244.0', 1], ['688245.0', 1], ['688246.0', 2]]

    return ret

##__________________________________________________________________||
def change_job_priority(ids, priority=10, n_at_a_time=500):

    # http://research.cs.wisc.edu/htcondor/manual/v7.8/2_6Managing_Job.html#sec:job-prio

    ids_split = split_ids(ids, n=n_at_a_time)
    for ids_sub in ids_split:
        procargs = ['condor_prio', '-p', str(priority)] + ids_sub
        try_executing_until_succeed(procargs)

##__________________________________________________________________||
def split_ids(ids, n=500):
    # e.g.,
    # ids = [3158174', '3158175', '3158176', '3158177', '3158178']
    # n = 2
    # return [[3158174', '3158175'], ['3158176', '3158177'], ['3158178']]
    return [ids[i:(i + n)] for i in range(0, len(ids), n)]

##__________________________________________________________________||
