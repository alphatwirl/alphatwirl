# Tai Sakuma <tai.sakuma@gmail.com>
import os
import gzip
import shutil

try:
   import cPickle as pickle
except:
   import pickle

import pytest

import alphatwirl
import alphatwirl.concurrently
from alphatwirl.concurrently import TaskPackage

##__________________________________________________________________||
@pytest.fixture()
def env():
   # add path to alphatwirl to PYTHONPATH in env for subprocess
   env = os.environ.copy()
   alphatwirl_path = os.path.dirname(os.path.dirname(os.path.abspath(alphatwirl.__file__)))
   if 'PYTHONPATH' in env:
      env['PYTHONPATH'] = '{}:{}'.format(alphatwirl_path, env['PYTHONPATH'])
   else:
      env['PYTHONPATH'] = alphatwirl_path
   return env

@pytest.fixture()
def workingarea_path(tmpdir_factory):
   ret = str(tmpdir_factory.mktemp(''))
   src = os.path.join(os.path.dirname(alphatwirl.concurrently.__file__), 'run.py')
   dest = os.path.join(ret, 'run.py')
   shutil.copy(src, dest)
   return ret

##__________________________________________________________________||
def task_null(*args, **kwargs):
   return

@pytest.fixture()
def package_rel_path_task_null(workingarea_path):

   ret = 'task_00009.p.gz'

   package = TaskPackage(
      task = task_null,
      args = [ ],
      kwargs =   { }
   )

   path = os.path.join(workingarea_path, ret)
   with gzip.open(path, 'wb') as f:
      pickle.dump(package, f, protocol = pickle.HIGHEST_PROTOCOL)

   return ret

@pytest.mark.script_launch_mode('subprocess')
def test_run_task_null(script_runner, workingarea_path, package_rel_path_task_null, env):

   script_path = os.path.join('.', 'run.py')
   args = [package_rel_path_task_null]
   ret = script_runner.run(script_path, *args, cwd=workingarea_path, env=env)
   assert ret.success
   assert '' == ret.stderr
   assert '' == ret.stdout

##__________________________________________________________________||
def task_raise(*args, **kwargs):
    raise Exception('test error from task_raise()')

@pytest.fixture()
def package_rel_path_task_raise(workingarea_path):

   ret = 'task_00009.p.gz'

   package = TaskPackage(
      task = task_raise,
      args = [ ],
      kwargs =   { }
   )

   path = os.path.join(workingarea_path, ret)
   with gzip.open(path, 'wb') as f:
      pickle.dump(package, f, protocol = pickle.HIGHEST_PROTOCOL)

   return ret

@pytest.mark.script_launch_mode('subprocess')
def test_run_task_null(script_runner, workingarea_path, package_rel_path_task_raise, env):

   script_path = os.path.join('.', 'run.py')
   args = [package_rel_path_task_raise]
   ret = script_runner.run(script_path, *args, cwd=workingarea_path, env=env)
   assert ret.success == False
   assert 'Exception:' in ret.stderr
   assert '' == ret.stdout

##__________________________________________________________________||
