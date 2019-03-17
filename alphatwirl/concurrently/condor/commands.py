# Tai Sakuma <sakuma@cern.ch>
import re

from .exec_util import try_executing_until_succeed, exec_command

##__________________________________________________________________||
def submit_jobs(job_desc, cwd=None):

    procargs = ['condor_submit']

    stdout = try_executing_until_succeed(procargs, input_=job_desc, cwd=cwd)
    stdout = '\n'.join(stdout)
    # e.g., '3 job(s) submitted to cluster 3158626.'

    regex = re.compile(r"(\d+) job\(s\) submitted to cluster (\d+)", re.MULTILINE)
    match = regex.search(stdout)
    groups = match.groups()
    # e.g., ('3', '3158626')

    njobs, clusterid = groups
    njobs = int(njobs)

    procid = ['{}'.format(i) for i in range(njobs)]
    # e.g., ['0', '1', '2', '3']

    clusterprocids = ['{}.{}'.format(clusterid, i) for i in procid]
    # e.g., ['3158626.0', '3158626.1', '3158626.2', '3158626.3']

    return clusterprocids

##__________________________________________________________________||
def query_status_for(clusterids, n_at_a_time=500):

    ids_split = split_list_into_chunks(clusterids, n=n_at_a_time)
    stdout = [ ]
    for ids_sub in ids_split:
        procargs = ['condor_q'] + ids_sub
        procargs += ['-format', '%d.', 'ClusterId',
                     '-format', '%d ', 'ProcId',
                     '-format', '%-2s\n', 'JobStatus']
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

    ids_split = split_list_into_chunks(ids, n=n_at_a_time)
    for ids_sub in ids_split:
        procargs = ['condor_prio', '-p', str(priority)] + ids_sub
        try_executing_until_succeed(procargs)

##__________________________________________________________________||
def terminate_jobs(clusterids, n_at_a_time=500):
    ids_split = split_list_into_chunks(clusterids)
    for ids_sub in ids_split:
        procargs = ['condor_rm'] + ids_sub
        try:
            exec_command(procargs)
        except RuntimeError:
            pass

##__________________________________________________________________||
def split_list_into_chunks(l, n=500):
    # e.g.,
    # l = [3158174', '3158175', '3158176', '3158177', '3158178']
    # n = 2
    # return [[3158174', '3158175'], ['3158176', '3158177'], ['3158178']]
    return [l[i:(i + n)] for i in range(0, len(l), n)]

##__________________________________________________________________||
