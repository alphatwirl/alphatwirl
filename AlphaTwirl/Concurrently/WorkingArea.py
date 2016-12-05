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
        self.path = self._prepare_dir(dir)
        self.last_package_index = -1 # so it starts from 0

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

        tar = tarfile.open(os.path.join(self.path, 'python_modules.tar.gz'), 'w:gz')

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

        self.last_package_index += 1
        package_index = self.last_package_index

        package_path = 'task_{:05d}.p'.format(package_index)
        # relative to dirpath, e.g., 'task_00009.p'

        package_fullpath = os.path.join(self.path, package_path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p'

        f = open(package_fullpath, 'wb')
        pickle.dump(package, f)
        f.close()

        return package_index, package_path

    def collect_result(self, package_index):

        dirname = 'task_{:05d}'.format(package_index)
        # e.g., 'task_00009'

        result_path = os.path.join(self.path, 'results', dirname, 'result.p')
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p'

        f = open(result_path, 'rb')
        result = pickle.load(f)

        return result


##__________________________________________________________________||
