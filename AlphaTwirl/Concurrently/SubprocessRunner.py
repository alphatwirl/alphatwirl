# Tai Sakuma <tai.sakuma@cern.ch>
import os
import subprocess
import collections

##__________________________________________________________________||
class SubprocessRunner(object):
    def __init__(self, pipe = False):
        self.running_procs = collections.deque()
        self.pipe = pipe

    def run(self, taskdir, package_path):

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

    def wait(self):
        ret = [ ] # a list of pairs of stdout and stderr,
                  # e.g., [(stdout, stderr), (stdout, stderr)]

        while self.running_procs:
            proc = self.running_procs.popleft()
            ret.append(proc.communicate())
        return ret

    def terminate(self):
        while self.running_procs:
            proc = self.running_procs.popleft()
            proc.terminate()

##__________________________________________________________________||
