# Tai Sakuma <tai.sakuma@cern.ch>
import os
import shutil
import pickle
import datetime
import tempfile
import imp
import tarfile

##__________________________________________________________________||
class WorkingArea(object):
    """
        Args:
        dir (str): a path to a directory in which a new directory will be created

    """

    def __init__(self, dir):
        self.dirpath = self._prepare_dir(dir)
        self.last_taskindex = -1 # so it starts from 0

    def _prepare_dir(self, path):

        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        dirpath = tempfile.mkdtemp(prefix = prefix, dir = path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        # copy run.py to the task dir
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, 'run.py')
        shutil.copy(src, dirpath)

        return dirpath

    def put_python_modules(self, modules):

        if not modules: return

        tar = tarfile.open(os.path.join(self.dirpath, 'python_modules.tar.gz'), 'w:gz')

        def tar_filter(tarinfo):
            exclude_extensions = ('.pyc', )
            exclude_names = ('.git', )
            if os.path.splitext(tarinfo.name)[1] in exclude_extensions: return None
            if os.path.basename(tarinfo.name) in exclude_names: return None
            return tarinfo

        for module in modules:
            imp_tuple = imp.find_module(module)
            path = imp_tuple[1]
            arcname = os.path.join('python_modules', module + imp_tuple[2][0])
            tar.add(path, arcname = arcname, filter = tar_filter)
        tar.close()

    def put_package(self, package):

        self.last_taskindex += 1
        task_idx = self.last_taskindex

        package_path = 'task_{:05d}.p'.format(task_idx)
        # relative to dirpath, e.g., 'task_00009.p'

        package_fullpath = os.path.join(self.dirpath, package_path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p'

        f = open(package_fullpath, 'wb')
        pickle.dump(package, f)

        return task_idx, package_path

    def collect_result(self, task_idx):

        dirname = 'task_{:05d}'.format(task_idx)
        # e.g., 'task_00009'

        result_path = os.path.join(self.dirpath, 'results', dirname, 'result.p')
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p'

        f = open(result_path, 'rb')
        result = pickle.load(f)

        return result


##__________________________________________________________________||
class TaskPackageDropbox(object):
    def __init__(self, dispatcher, path, put_alphatwirl = True, user_modules = ()):
        self.dispatcher = dispatcher
        self.path = path
        self.python_modules = list(user_modules)
        if put_alphatwirl: self.python_modules.append('AlphaTwirl')

    def open(self):
        self.workingArea = WorkingArea(self.path)
        self.workingArea.put_python_modules(self.python_modules)
        self.taskindices = [ ]

    def put(self, package):
        taskindex, package_path = self.workingArea.put_package(package)
        self.taskindices.append(taskindex)
        self.dispatcher.run(self.workingArea.dirpath, package_path)

    def receive(self):
        self.dispatcher.wait()
        results = [self.workingArea.collect_result(i) for i in self.taskindices]
        self.taskindices[:] = [ ]
        return results

    def close(self):
        self.dispatcher.terminate()

##__________________________________________________________________||
