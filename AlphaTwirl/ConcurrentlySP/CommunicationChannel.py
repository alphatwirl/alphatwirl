# Tai Sakuma <tai.sakuma@cern.ch>
import os
import subprocess
import collections

from ..ProgressBar import NullProgressMonitor
from ..mkdir_p import mkdir_p

from .TaskPackageDropbox import TaskPackageDropbox

##__________________________________________________________________||
TaskPackage = collections.namedtuple(
    'TaskPackage',
    'task progressReporter args kwargs'
)

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
class CommunicationChannel(object):
    """An implementation of concurrency with subprocess.

    """
    def __init__(self, progressMonitor = None, tmpdir = '_ccsp_temp'):
        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor
        self.tmpdir = tmpdir
        mkdir_p(self.tmpdir)
        self.dropbox = TaskPackageDropbox(
            dispatcher = TaskDispatcher(),
            path = self.tmpdir
        )

    def begin(self):
        self.dropbox.open()

    def put(self, task, *args, **kwargs):
        package = TaskPackage(
            task = task,
            progressReporter = self.progressMonitor.createReporter(),
            args = args,
            kwargs =  kwargs
        )
        self.dropbox.put(package)

    def receive(self):
        results = self.dropbox.receive()
        return results

    def end(self):
        self.dropbox.close()

##__________________________________________________________________||
