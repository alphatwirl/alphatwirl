# Tai Sakuma <tai.sakuma@cern.ch>
import os
import subprocess
import collections

##__________________________________________________________________||
class SubprocessRunner(object):
    def __init__(self, pipe = False):
        self.running_procs = collections.deque()
        self.pipe = pipe

    def run(self, workingArea, package_index):

        taskdir = workingArea.path

        package_path = workingArea.package_path(package_index)

        # run_script = os.path.join(taskdir, 'run.py') # This doesn't work.
                                                       # It contradicts with the document https://docs.python.org/2/library/subprocess.html
                                                       # The program's path needs to be relative to cwd
        run_script = os.path.join('.', 'run.py') # This works

        args = [run_script, package_path]
        proc = subprocess.Popen(
            args,
            stdout = subprocess.PIPE if self.pipe else None,
            stderr = subprocess.PIPE if self.pipe else None,
            cwd = taskdir
        )
        self.running_procs.append(proc)
        return proc.pid # as runid

    def poll(self):
        """check if the jobs are running and return a list of pids for
        finished jobs

        """
        finished_procs = [p for p in self.running_procs if p.poll() is not None]
        self.running_procs = [p for p in self.running_procs if p not in finished_procs]

        for proc in finished_procs:
            stdout, stderr = proc.communicate()
            ## proc.communicate() returns (stdout, stderr) when
            ## self.pipe = True. Otherwise they are (None, None)

        finished_pids = [p.pid for p in  finished_procs]
        return finished_pids # as runids

    def wait(self):
        """wait until all jobs finish and return a list of pids
        """
        finished_pids = [ ]
        while self.running_procs:
            finished_pids.extend(self.poll())
        return finished_pids # as runids

    def failed_runids(self, runids):
        pass

    def terminate(self):
        while self.running_procs:
            proc = self.running_procs.popleft()
            proc.terminate()

##__________________________________________________________________||
