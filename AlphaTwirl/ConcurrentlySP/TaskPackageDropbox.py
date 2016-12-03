# Tai Sakuma <tai.sakuma@cern.ch>
import os
import shutil
import pickle
import datetime
import tempfile

##__________________________________________________________________||
class TaskPackageDropbox(object):
    def __init__(self, dispatcher, path):
        self.dispatcher = dispatcher
        self.path = path

    def open(self):
        self.workdir = self._prepare_workdir(self.path)
        self.taskindices = [ ]
        self.last_taskindex = -1 # so it starts from 0

    def put(self, package):
        self.last_taskindex += 1
        taskindex = self.last_taskindex
        package_path = self._save_package_in_workdir(taskindex, package, self.workdir)
        self.taskindices.append(taskindex)
        self.dispatcher.run(self.workdir, package_path)

    def receive(self):
        self.dispatcher.wait()
        results = [self._collect_result(i, self.workdir) for i in self.taskindices]
        self.taskindices[:] = [ ]
        return results

    def close(self):
        self.dispatcher.terminate()

    def _prepare_workdir(self, path):

        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        workdir = tempfile.mkdtemp(prefix = prefix, dir = path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        # copy run.py to the task dir
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, 'run.py')
        shutil.copy(src, workdir)

        return workdir

    def _save_package_in_workdir(self, task_idx, package, workdir):
        package_path = 'task_{:05d}.p'.format(task_idx)
        # relative to workdir, e.g., 'task_00009.p'

        package_fullpath = os.path.join(workdir, package_path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p'

        f = open(package_fullpath, 'wb')
        pickle.dump(package, f)

        return package_path

    def _collect_result(self, task_idx, workdir):

        dirname = 'task_{:05d}'.format(task_idx)
        # e.g., 'task_00009'

        result_path = os.path.join(workdir, 'results', dirname, 'result.p')
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p'

        f = open(result_path, 'rb')
        result = pickle.load(f)

        return result


##__________________________________________________________________||
