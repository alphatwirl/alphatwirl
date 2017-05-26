# Tai Sakuma <tai.sakuma@cern.ch>
import os
import shutil
import datetime
import tempfile
import imp
import logging
import tarfile
import gzip

try:
   import cPickle as pickle
except:
   import pickle

##__________________________________________________________________||
class WorkingArea(object):
    """
        Args:
        dir (str): a path to a directory in which a new directory will be created

    """

    def __init__(self, dir, python_modules):
        self.topdir = dir
        self.python_modules = python_modules
        self.path = None
        self.last_package_index = None

    def __repr__(self):
        return '{}(topdir = {!r}, python_modules = {!r}, path = {!r}, last_package_index = {!r})'.format(
            self.__class__.__name__,
            self.topdir, self.python_modules, self.path, self.last_package_index
        )

    def open(self):
        self.path = self._prepare_dir(self.topdir)
        self._put_python_modules(self.python_modules)
        self.last_package_index = -1 # so it starts from 0

    def put_package(self, package):

        self.last_package_index += 1
        package_index = self.last_package_index

        package_path = self.package_path(package_index)
        # relative to self.path, e.g., 'task_00009.p.gz'

        package_fullpath = os.path.join(self.path, package_path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        f = gzip.open(package_fullpath, 'wb')
        pickle.dump(package, f, protocol = pickle.HIGHEST_PROTOCOL)
        f.close()

        return package_index

    def package_path(self, package_index):
        return 'task_{:05d}.p.gz'.format(package_index)

    def collect_result(self, package_index):

        dirname = 'task_{:05d}'.format(package_index)
        # e.g., 'task_00009'

        result_path = os.path.join(self.path, 'results', dirname, 'result.p.gz')
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        try:
           f = gzip.open(result_path, 'rb')
           result = pickle.load(f)
        except (IOError, EOFError) as e:
           logger = logging.getLogger(__name__)
           logger.warning(e)
           return None

        return result

    def close(self):
        self.path = None
        self.last_package_index = None

    def _prepare_dir(self, dir):

        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        path = tempfile.mkdtemp(prefix = prefix, dir = dir)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        # copy run.py to the task dir
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, 'run.py')
        shutil.copy(src, path)

        return path

    def _put_python_modules(self, modules):

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

##__________________________________________________________________||
