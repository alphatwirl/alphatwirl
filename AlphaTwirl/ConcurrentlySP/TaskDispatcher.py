# Tai Sakuma <tai.sakuma@cern.ch>
import os
import subprocess
import collections

##__________________________________________________________________||
class TaskDispatcher(object):
    def __init__(self):
        self.running_procs = collections.deque()

    def run(self, taskdir, package_path):
        run_script = os.path.join(taskdir, 'run.py')
        args = [run_script, package_path]
        proc = subprocess.Popen(args)
        self.running_procs.append(proc)

    def wait(self):
        while self.running_procs:
            proc = self.running_procs.popleft()
            proc.communicate()

    def terminate(self):
        while self.running_procs:
            proc = self.running_procs.popleft()
            proc.terminate()

##__________________________________________________________________||
