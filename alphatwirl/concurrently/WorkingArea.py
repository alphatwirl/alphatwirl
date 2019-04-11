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

from alphatwirl.misc.deprecation import _deprecated, _renamed_class_method_option

##__________________________________________________________________||
class WorkingArea(object):
    """A working area for tasks

    This is an area where pickled tasks, pickled results, archived
    Python modules, etc are placed.

    Parameters
    ----------
    topdir : str
        a path to a directory in which a new directory will be created
    python_modules :list
        names of Python modules to be shipped to worker nodes

    """

    @_renamed_class_method_option(old='dir', new='topdir')
    def __init__(self, topdir, python_modules=None):

        if python_modules is None:
            python_modules = ()

        self.topdir = topdir
        self.python_modules = python_modules
        self.path = None
        self.last_package_index = -1 # so it starts from 0

        self.executable = 'run.py'
        self.extra_input_files = set()

    def __repr__(self):
        name_value_pairs = (
            ('topdir', self.topdir),
            ('python_modules', self.python_modules),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def open(self):
        """Open the working area

        Returns
        -------
        None
        """

        self.path = self._prepare_dir(self.topdir)
        self._copy_executable(area_path=self.path)
        self._save_logging_levels(area_path=self.path)
        self._put_python_modules(modules=self.python_modules, area_path=self.path)

    def _prepare_dir(self, dir):

        alphatwirl.mkdir_p(dir)

        prefix = 'tpd_{:%Y%m%d_%H%M%S}_'.format(datetime.datetime.now())
        # e.g., 'tpd_20161129_122841_'

        path = tempfile.mkdtemp(prefix=prefix, dir=dir)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF'

        return path

    def _copy_executable(self, area_path):
        thisdir = os.path.dirname(__file__)
        src = os.path.join(thisdir, self.executable)
        shutil.copy(src, area_path)

    def _save_logging_levels(self, area_path):
        logger_names = logging.Logger.manager.loggerDict.keys()
        loglevel_dict = {l: logging.getLogger(l).getEffectiveLevel() for l in logger_names}

        filename = 'logging_levels.json.gz'
        path = os.path.join(area_path, filename)

        json_str = json.dumps(loglevel_dict, indent=4, sort_keys=True)
        json_str = re.sub(r' *\n', '\n', json_str, flags=re.MULTILINE)
        json_str += "\n"
        json_bytes = json_str.encode('utf-8')
        with gzip.open(path, "w") as f:
            f.write(json_bytes)

        self.extra_input_files.add(filename)

    def _put_python_modules(self, modules, area_path):

        if not modules: return

        filename = 'python_modules.tar.gz'
        path = os.path.join(area_path, filename)
        tar = tarfile.open(path, 'w:gz')

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

        self.extra_input_files.add(filename)

    def close(self):
        """Close the working area

        Returns
        -------
        None

        """
        self.path = None

    def put_package(self, package):
        """Put a package

        Parameters
        ----------
        package :
            a task package

        Returns
        -------
        int
            A package index

        """

        self.last_package_index += 1
        package_index = self.last_package_index

        package_fullpath = self.package_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        with gzip.open(package_fullpath, 'wb') as f:
            pickle.dump(package, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

        result_fullpath = self.result_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        result_dir = os.path.dirname(result_fullpath)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009'

        alphatwirl.mkdir_p(result_dir)

        return package_index

    def collect_result(self, package_index):
        """Collect the result of a task

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        obj
            The result of the task

        """

        result_fullpath = self.result_fullpath(package_index)
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        try:
            with gzip.open(result_fullpath, 'rb') as f:
                result = pickle.load(f)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(e)
            return None

        return result

    def package_relpath(self, package_index):
        """Returns the relative path of the package

        This method returns the path to the package relative to the
        top dir of the working area. This method simply constructs the
        path based on the convention and doesn't check if the package
        actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the relative path to the package

        """

        ret = 'task_{:05d}.p.gz'.format(package_index)
        # e.g., 'task_00009.p.gz'

        return ret

    @_deprecated(msg='use package_relpath instead')
    def package_path(self, package_index):
        return self.package_relpath(package_index)

    def package_fullpath(self, package_index):
        """Returns the full path of the package

        This method returns the full path to the package. This method
        simply constructs the path based on the convention and doesn't
        check if the package actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the full path to the package

        """

        ret = os.path.join(self.path, self.package_relpath(package_index))
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/task_00009.p.gz'

        return ret

    def result_relpath(self, package_index):
        """Returns the relative path of the result

        This method returns the path to the result relative to the
        top dir of the working area. This method simply constructs the
        path based on the convention and doesn't check if the result
        actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the relative path to the result

        """

        dirname = 'task_{:05d}'.format(package_index)
        # e.g., 'task_00009'

        ret = os.path.join('results', dirname, 'result.p.gz')
        # e.g., 'results/task_00009/result.p.gz'

        return ret

    def result_fullpath(self, package_index):
        """Returns the full path of the result

        This method returns the full path to the result. This method
        simply constructs the path based on the convention and doesn't
        check if the result actually exists.

        Parameters
        ----------
        package_index :
            a package index

        Returns
        -------
        str
            the full path to the result

        """

        ret = os.path.join(self.path, self.result_relpath(package_index))
        # e.g., '{path}/tpd_20161129_122841_HnpcmF/results/task_00009/result.p.gz'

        return ret

##__________________________________________________________________||
