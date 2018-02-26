# Tai Sakuma <tai.sakuma@gmail.com>
import os
import shutil
import datetime
import tempfile
import imp
import logging
import tarfile
import gzip
import json
import re

try:
    import cPickle as pickle
except:
    import pickle

import alphatwirl

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
        return '{}(topdir={!r}, python_modules={!r}, path={!r}, last_package_index={!r})'.format(
            self.__class__.__name__,
            self.topdir, self.python_modules, self.path, self.last_package_index
        )

    def open(self):
        self.path = self._prepare_dir(self.topdir)
        self._copy_run_py(area_path=self.path)
        self._save_logging_levels(area_path=self.path)
        self._put_python_modules(modules=self.python_modules, area_path=self.path)
        self.last_package_index = -1 # so it starts from 0

    def put_package(self, package):

        self.last_package_index += 1
        package_index = self.last_package_index

        package_path = self.package_path(package_index)
        # relative to self.path, e.g., 'task_00009.p.gz'

        package_fullpath = os.path.join(self.path, package_path)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        with gzip.open(package_fullpath, 'wb') as f:
           pickle.dump(package, f, protocol=pickle.HIGHEST_PROTOCOL)
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
           with gzip.open(result_path, 'rb') as f:
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

        alphatwirl.mkdir_p(dir)

        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        path = tempfile.mkdtemp(prefix=prefix, dir=dir)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        return path

    def _copy_run_py(self, area_path):
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, 'run.py')
        shutil.copy(src, area_path)

    def _save_logging_levels(self, area_path):
        logger_names = logging.Logger.manager.loggerDict.keys()
        loglevel_dict = {l: logging.getLogger(l).getEffectiveLevel() for l in logger_names}

        json_str = json.dumps(loglevel_dict, indent=4, sort_keys=True)
        json_str = re.sub(r' *\n', '\n', json_str, flags=re.MULTILINE)
        json_str += "\n"
        json_bytes = json_str.encode('utf-8')
        path = os.path.join(area_path, 'logging_levels.json.gz')
        with gzip.open(path, "w") as f:
            f.write(json_bytes)

    def _put_python_modules(self, modules, area_path):

        if not modules: return

        tar = tarfile.open(os.path.join(area_path, 'python_modules.tar.gz'), 'w:gz')

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
            tar.add(path, arcname=arcname, filter=tar_filter)
        tar.close()

##__________________________________________________________________||
