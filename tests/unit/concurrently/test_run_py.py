import unittest
import os
import tempfile
import shutil
import gzip
import subprocess

try:
   import cPickle as pickle
except:
   import pickle

import alphatwirl
import alphatwirl.concurrently
from alphatwirl.concurrently import TaskPackage

##__________________________________________________________________||
def task_null(*args, **kwargs):
    return

##__________________________________________________________________||
def task_raise(*args, **kwargs):
    raise Exception('test error from task_raise()')

##__________________________________________________________________||
class TestRunPy(unittest.TestCase):

    def setUp(self):
        self.tempdir_path = tempfile.mkdtemp()
        self.run_py_path = self._copy_run_py_to_tempdir()
        self.env = self._build_env_for_subprocess()

    def _copy_run_py_to_tempdir(self):
        src = os.path.join(os.path.dirname(alphatwirl.concurrently.__file__), 'run.py')
        dest = os.path.join(self.tempdir_path, 'run.py')
        shutil.copy(src, dest)
        return dest

    def _build_env_for_subprocess(self):
        # add path to alphatwirl to PYTHONPATH in env for subprocess
        env = os.environ.copy()
        alphatwirl_path = os.path.dirname(os.path.dirname(os.path.abspath(alphatwirl.__file__)))
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = '{}:{}'.format(alphatwirl_path, env['PYTHONPATH'])
        else:
            env['PYTHONPATH'] = alphatwirl_path
        return env

    def tearDown(self):
        shutil.rmtree(self.tempdir_path)
        pass

    def test_run_task_null(self):
        package = TaskPackage(
            task = task_null,
            args = [ ],
            kwargs =   { }

        )
        package_path = os.path.join(self.tempdir_path, 'task_00009.p.gz')
        with gzip.open(package_path, 'wb') as f:
            pickle.dump(package, f, protocol = pickle.HIGHEST_PROTOCOL)
            f.close()

        proc = subprocess.Popen(
            [os.path.join('.', 'run.py'), 'task_00009.p.gz'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            cwd = self.tempdir_path,
            env = self.env
        )
        stdout, stderr = proc.communicate()

    def test_run_task_raise(self):
        package = TaskPackage(
            task = task_raise,
            args = [ ],
            kwargs =   { }

        )
        package_path = os.path.join(self.tempdir_path, 'task_00009.p.gz')
        with gzip.open(package_path, 'wb') as f:
            pickle.dump(package, f, protocol = pickle.HIGHEST_PROTOCOL)
            f.close()

        proc = subprocess.Popen(
            [os.path.join('.', 'run.py'), 'task_00009.p.gz'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            cwd = self.tempdir_path,
            env = self.env
        )
        stdout, stderr = proc.communicate()
        self.assertIn('Exception:'.encode(), stderr)

##__________________________________________________________________||

