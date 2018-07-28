# Tai Sakuma <tai.sakuma@gmail.com>
import os
import gzip

try:
   import cPickle as pickle
except:
   import pickle

import pytest

import alphatwirl

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
   return ret

##__________________________________________________________________||
class Reader(object):
   def end(self):
      pass

@pytest.fixture()
def pickled_reader_path(workingarea_path):

   reader = Reader()

   ret = os.path.join(workingarea_path, 'reader.p.gz')
   with gzip.open(ret, 'wb') as f:
      pickle.dump(reader, f, protocol = pickle.HIGHEST_PROTOCOL)

   return ret

@pytest.mark.script_launch_mode('subprocess')
def test_run(script_runner, pickled_reader_path, env):

   script_path = os.path.join(os.path.dirname(alphatwirl.datasetloop.__file__), 'resume.py')
   args = [pickled_reader_path]
   ret = script_runner.run(script_path, *args, env=env)
   assert ret.success
   assert '' == ret.stdout

   # assert '' == ret.stderr
   ## commented out because of "RuntimeWarning" in travis
   ## https://travis-ci.org/alphatwirl/alphatwirl/jobs/409237073
   ## E AssertionError: assert '' == '/home/travis/miniconda/envs...ok( name,
   ## *args, **kwds )\n'
   ## E + /home/travis/miniconda/envs/testenv/lib/ROOT.py:301: RuntimeWarning:
   ## numpy.dtype size changed, may indicate binary incompatibility. Expected
   ## 96, got 88


##__________________________________________________________________||
