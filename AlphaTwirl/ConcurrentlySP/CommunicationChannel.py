# Tai Sakuma <tai.sakuma@cern.ch>
import os
import shutil
import subprocess
import pickle
import datetime
import tempfile
import collections
from operator import itemgetter

from ..ProgressBar import NullProgressMonitor
from ..mkdir_p import mkdir_p

##__________________________________________________________________||
TaskPackage = collections.namedtuple(
    'TaskPackage',
    'index task progressReporter args kwargs'
)

##__________________________________________________________________||
class TaskDirectory(object):
    def __init__(self, path):

        # create a task directory
        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        self.taskdir = tempfile.mkdtemp(prefix = prefix, dir = path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        # copy run.py to the task dir
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, 'run.py')
        shutil.copy(src, self.taskdir)

        self.task_idx = -1 # so it starts from 0
        self.running_task_idxs = collections.deque()

        self.package_path_dict = { }

    def put(self, package):

        task_idx = package.index

        basename = 'task_{:05d}.p'.format(task_idx)
        # e.g., 'task_00009.p'

        package_path = os.path.join(self.taskdir, basename)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p'

        f = open(package_path, 'wb')
        pickle.dump(package, f)

        self.package_path_dict[task_idx] = package_path

        self.running_task_idxs.append(task_idx)

        return task_idx

    def package_path(self, task_idx):
        return self.package_path_dict[task_idx]

    def receive(self):

        task_idx_result_pairs = [ ]
        while self.running_task_idxs:
            task_idx = self.running_task_idxs.popleft()
            result = self.get(task_idx)
            task_idx_result_pairs.append((task_idx, result))

        task_idx_result_pairs = sorted(task_idx_result_pairs, key = itemgetter(0))

        results = [result for idx, result in task_idx_result_pairs]

        return results

    def get(self, task_idx):

        dirname = 'task_{:05d}'.format(task_idx)
        # e.g., 'task_00009'

        result_path = os.path.join(self.taskdir, 'results', dirname, 'result.p')
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p'

        f = open(result_path, 'rb')
        result = pickle.load(f)

        return result

##__________________________________________________________________||
class TaskRunner(object):
    def __init__(self, taskDirectory):
        self.taskDirectory = taskDirectory
        self.running_procs = collections.deque()

    def run(self, task_idx):
        run_script = os.path.join(self.taskDirectory.taskdir, 'run.py')
        package_path = self.taskDirectory.package_path(task_idx)
        args = [run_script, package_path]
        ## proc = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
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
        self.taskDirectory = TaskDirectory(path = self.tmpdir)
        self.taskRunner = TaskRunner(taskDirectory = self.taskDirectory)

    def begin(self):
        pass

    def put(self, task, *args, **kwargs):
        self.taskDirectory.task_idx += 1
        package = TaskPackage(
            index = self.taskDirectory.task_idx,
            task = task,
            progressReporter = self.progressMonitor.createReporter(),
            args = args,
            kwargs =  kwargs
        )
        task_idx = self.taskDirectory.put(package)
        self.taskRunner.run(task_idx)

    def receive(self):
        self.taskRunner.wait()

        results = self.taskDirectory.receive()
        return results

    def end(self):
        self.taskRunner.terminate()

##__________________________________________________________________||
