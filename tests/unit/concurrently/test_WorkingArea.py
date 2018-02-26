# Tai Sakuma <tai.sakuma@gmail.com>
import os
import collections
import gzip

import pytest

try:
    import cPickle as pickle
except:
    import pickle

from alphatwirl.concurrently import WorkingArea
from alphatwirl import mkdir_p

##__________________________________________________________________||
## cannot be replaced with MagicMock because MagicMock is not picklable
MockPackage = collections.namedtuple('MockPackage', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

@pytest.fixture()
def obj(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp(''))
    tmpdir = os.path.join(tmpdir, '_ccsp_temp')
    return WorkingArea(dir=tmpdir, python_modules=('alphatwirl', ))

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_open(obj):
    assert obj.path is None
    assert obj.last_package_index is None

    obj.open()
    assert obj.path is not None
    assert -1 == obj.last_package_index
    assert os.path.isdir(obj.path)
    assert os.path.isfile(os.path.join(obj.path, 'run.py'))
    assert os.path.isfile(os.path.join(obj.path, 'logging_levels.json.gz'))
    assert os.path.isfile(os.path.join(obj.path, 'python_modules.tar.gz'))

def test_put_package(obj):

    obj.open()

    package1 = MockPackage(name='package1')
    package_index = obj.put_package(package1)
    package_path = obj.package_path(package_index)
    package_fullpath = os.path.join(obj.path, package_path)
    assert os.path.isfile(package_fullpath)
    with gzip.open(package_fullpath, 'rb') as f:
       assert package1 == pickle.load(f)

def test_collect_result(obj):

    obj.open()

    result = MockResult(name='result1')

    package_index = 9
    dirname = 'task_{:05d}'.format(package_index)
    result_dir = os.path.join(obj.path, 'results', dirname)
    mkdir_p(result_dir)
    result_path = os.path.join(result_dir, 'result.p.gz')
    with gzip.open(result_path, 'wb') as f:
       pickle.dump(result, f)
       f.close()

    assert result == obj.collect_result(package_index=package_index)

def test_collect_result_ioerror(obj):
   # the file 'result.p.gz' doesn't exist
   # gzip.open() raises IOFError

    obj.open()

    # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
    package_index = 9
    assert obj.collect_result(package_index=package_index) is None

def test_collect_result_eoferror(obj):
   # the file 'result.p.gz' is empty.
   # pickle.load() raises EOFError

    obj.open()

    package_index = 9
    dirname = 'task_{:05d}'.format(package_index)
    result_dir = os.path.join(obj.path, 'results', dirname)
    mkdir_p(result_dir)

    result_path = os.path.join(result_dir, 'result.p.gz')
    with open(result_path, 'wb') as f:
       f.close()

    assert obj.collect_result(package_index=package_index) is None

##__________________________________________________________________||

