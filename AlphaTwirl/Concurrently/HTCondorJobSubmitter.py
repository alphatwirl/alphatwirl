#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import os, sys
import argparse
import subprocess
import collections
import time
import textwrap
import getpass
import re
import logging

import AlphaTwirl

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
class HTCondorJobSubmitter(object):
    def __init__(self):

        self.job_desc_template = """
        Executable = {job_script}
        output = {out}
        error = {error}
        log = {log}
        {args}
        should_transfer_files = YES
        when_to_transfer_output = ON_EXIT
        transfer_input_files = {input_files}
        transfer_output_files = {output_files}
        Universe = vanilla
        notification = Error
        # Initialdir = {initialdir}
        getenv = True
        queue 1
        """
        self.job_desc_template = textwrap.dedent(self.job_desc_template).strip()

        self.clusterids_outstanding = [ ]
        self.clusterids_finished = [ ]

    def run(self, taskdir, package_path):

        cwd = os.getcwd()
        os.chdir(taskdir)

        resultdir_basename = os.path.splitext(package_path)[0]
        resultdir_basename = os.path.splitext(resultdir_basename)[0]
        resultdir = os.path.join('results', resultdir_basename)
        AlphaTwirl.mkdir_p(resultdir)

        input_files = [package_path, 'python_modules.tar.gz']
        input_files = [f for f in input_files if os.path.exists(f)]

        job_desc = self.job_desc_template.format(
            job_script = 'run.py',
            out = os.path.join(resultdir, 'stdout.txt'),
            error = os.path.join(resultdir, 'stderr.txt'),
            log = os.path.join(resultdir, 'log.txt'),
            args = 'Arguments = {}'.format(package_path),
            input_files = ', '.join(input_files),
            output_files = 'results',
            initialdir = 'to be determined',
        )

        procargs = [
            '/usr/bin/condor_submit',
            '-append', 'accounting_group=group_physics.hep',
            '-append', 'accounting_group_user={}'.format(getpass.getuser()),
        ]
        proc = subprocess.Popen(
            procargs,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        stdout, stderr = proc.communicate(job_desc)
        regex = re.compile("submitted to cluster (\d*)", re.MULTILINE)
        clusterid = regex.search(stdout).groups()[0]

        self.clusterids_outstanding.append(clusterid)

        os.chdir(cwd)

    def wait(self):

        change_job_priority(self.clusterids_outstanding, 10)

        sleep = 5

        while True:
            clusterid_status_list = query_status_for(self.clusterids_outstanding)

            if clusterid_status_list:
                clusterids, statuses = zip(*clusterid_status_list)
            else:
                clusterids, statuses = (), ()

            self.clusterids_finished.extend([i for i in self.clusterids_outstanding if i not in clusterids])
            self.clusterids_outstanding[:] = clusterids

            # logging
            counter = collections.Counter(statuses)
            messages = [ ]
            if counter:
                messages.append(', '.join(['{}: {}'.format(HTCONDOR_JOBSTATUS[k], counter[k]) for k in counter.keys()]))
            if self.clusterids_finished:
                messages.append('Finished {}'.format(len(self.clusterids_finished)))
            logger = logging.getLogger(__name__)
            logger.info(', '.join(messages))

            if not self.clusterids_outstanding: break

            time.sleep(sleep)

    def terminate(self):
        n_at_a_time = 500
        ids_split = [self.clusterids_outstanding[i:(i + n_at_a_time)] for i in range(0, len(self.clusterids_outstanding), n_at_a_time)]
        statuses = [ ]
        for ids_sub in ids_split:
            procargs = ['condor_rm'] + ids_sub
            stdout = try_executing_until_succeed(procargs)

##__________________________________________________________________||
def try_executing_until_succeed(procargs):

    sleep = 2
    logger = logging.getLogger(__name__)

    while True:

        # logging
        ellipsis = '...(({} letters))...'
        nfirst = 50
        nlast = 50
        command_display = '{} {}'.format(procargs[0], ' '.join([repr(a) for a in procargs[1:]]))
        if len(command_display) > nfirst + len(ellipsis) + nlast:
            command_display = '{}...(({} letters))...{}'.format(
                command_display[:nfirst],
                len(command_display) - (nfirst + nlast),
                command_display[-nlast:]
            )
        logger.debug('execute: {}'.format(command_display))

        #
        proc = subprocess.Popen(
            procargs,
            stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdout, stderr =  proc.communicate()
        success = not (proc.returncode or stderr)

        #
        if success: break

        #
        if stderr: logger.warning(stderr.strip())
        logger.warning('the command failed: {}. will try again in {} seconds'.format(command_display, sleep))

        #
        time.sleep(sleep)

    if not stdout: return [ ]
    return stdout.rstrip().split('\n')

##__________________________________________________________________||
def query_status_for(ids):

    n_at_a_time = 500
    ids_split = [ids[i:(i + n_at_a_time)] for i in range(0, len(ids), n_at_a_time)]
    stdout = [ ]
    for ids_sub in ids_split:
        procargs = ['condor_q'] + ids_sub + ['-format', '%-2s ', 'ClusterId', '-format', '%-2s\n', 'JobStatus']
        stdout.extend(try_executing_until_succeed(procargs))

    # e.g., stdout = ['688244 1 ', '688245 1 ', '688246 2 ']

    ret = [l.strip().split() for l in stdout]
    # e.g., [['688244', '1'], ['688245', '1'], ['688246', '2']]

    ret = [[e[0], int(e[1])] for e in ret]
    # a list of [clusterid, status]
    # e.g., [['688244', 1], ['688245', 1], ['688246', 2]]

    return ret

##__________________________________________________________________||
def change_job_priority(ids, priority = 10):

    # http://research.cs.wisc.edu/htcondor/manual/v7.8/2_6Managing_Job.html#sec:job-prio

    n_at_a_time = 500
    ids_split = [ids[i:(i + n_at_a_time)] for i in range(0, len(ids), n_at_a_time)]
    for ids_sub in ids_split:
        procargs = ['condor_prio', '-p', str(priority)] + ids_sub
        try_executing_until_succeed(procargs)

##__________________________________________________________________||
def sample_ids(n = -1):
    # to be deleted

    procargs = ['condor_q', '-format', '%-2s\n', 'ClusterId']
    stdout = try_executing_until_succeed(procargs)
    sample_ids = [l.strip() for l in stdout]

    if n == -1:
        return sample_ids

    sample_ids = sample_ids[0:n] if len(sample_ids) >= n else sample_ids
    return sample_ids

##__________________________________________________________________||
