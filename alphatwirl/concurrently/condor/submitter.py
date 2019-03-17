#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import os
import time
import collections
import logging

from alphatwirl.misc.removal import _removed_class_method_option

from .commands import submit_jobs, query_status_for, change_job_priority, terminate_jobs

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

        # TODO: make configurable
        clusterids = clusterprocids2clusterids(clusterprocids)
        for clusterid in clusterids:
            change_job_priority([clusterid], 10)

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
        terminate_jobs(clusterids)

##__________________________________________________________________||
def clusterprocids2clusterids(clusterprocids):
    # e.g., ['3764857.0', '3764858.0', '3764858.1', '3764858.2']

    ret = sorted(list(set([i.split('.')[0] for i in clusterprocids])))
    # e.g., ['3764857', '3764858']

    return ret

##__________________________________________________________________||
