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
        run_script = os.path.join(taskdir, 'run.py')
        package_fullpath = os.path.join(taskdir, package_path)
        args = [run_script, package_fullpath]
        proc = subprocess.Popen(
            args,
            stdout = subprocess.PIPE if self.pipe else None,
            stderr = subprocess.PIPE if self.pipe else None,
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
