# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import logging
import collections
import gzip

try:
    import cPickle as pickle
except:
    import pickle

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import WorkingArea
from alphatwirl import mkdir_p

##__________________________________________________________________||
## cannot be replaced with mock.Mock because mock.Mock is not picklable
MockPackage = collections.namedtuple('MockPackage', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
@pytest.fixture()
def topdir(tmpdir_factory):
    ret = str(tmpdir_factory.mktemp(''))
    ret = os.path.join(ret, '_ccsp_temp')
    return ret

##__________________________________________________________________||
def test_renamed(topdir, caplog):
    with caplog.at_level(logging.WARNING):
        obj = WorkingArea(dir=topdir, python_modules=('alphatwirl', ))

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'WorkingArea' in caplog.records[0].name
    assert 'renamed' in caplog.records[0].msg

##__________________________________________________________________||
@pytest.fixture()
def obj(topdir):
    return WorkingArea(topdir=topdir, python_modules=('alphatwirl', ))

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)


def test_deprecated_package_path(obj, caplog):
    with caplog.at_level(logging.WARNING):
        obj.package_path(1)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'WorkingArea' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

def test_package_relpath(obj):
    assert 'task_00001.p.gz' == obj.package_relpath(1)

def test_package_fullpath(obj):
    obj.open()
    assert os.path.join(obj.path, 'task_00001.p.gz') == obj.package_fullpath(1)

def test_result_relpath(obj):
    assert os.path.join('results', 'task_00001' , 'result.p.gz') == obj.result_relpath(1)

def test_result_fullpath(obj):
    obj.open()
    assert os.path.join(obj.path, 'results', 'task_00001' , 'result.p.gz') == obj.result_fullpath(1)

def test_open(obj):
    assert obj.path is None

    obj.open()
    assert obj.path is not None
    assert -1 == obj.last_package_index
    assert os.path.isdir(obj.path)
    assert os.path.isfile(os.path.join(obj.path, 'run.py'))
    assert os.path.isfile(os.path.join(obj.path, 'logging_levels.json.gz'))
    assert os.path.isfile(os.path.join(obj.path, 'python_modules.tar.gz'))

def test_query(obj):
    obj.open()
    assert 'run.py' == obj.executable
    assert set([
        'python_modules.tar.gz',
        'logging_levels.json.gz']) == obj.extra_input_files

def test_query_no_python_module(topdir):
    obj = WorkingArea(topdir=topdir)
    obj.open()
    assert 'run.py' == obj.executable
    assert set(['logging_levels.json.gz']) == obj.extra_input_files

def test_put_package(obj):

    obj.open()

    package1 = MockPackage(name='package1')
    package_index = obj.put_package(package1)
    package_fullpath = obj.package_fullpath(package_index)
    assert os.path.isfile(package_fullpath)
    with gzip.open(package_fullpath, 'rb') as f:
       assert package1 == pickle.load(f)

    result_fullpath = obj.result_fullpath(package_index)
    result_dir = os.path.dirname(result_fullpath)
    assert not os.path.exists(result_fullpath)
    assert os.path.isdir(result_dir)

def test_collect_result(obj):

    obj.open()

    result = MockResult(name='result1')

    package_index = 9
    result_fullpath = obj.result_fullpath(package_index)
    mkdir_p(os.path.dirname(result_fullpath))
    with gzip.open(result_fullpath, 'wb') as f:
       pickle.dump(result, f)
       f.close()

    assert result == obj.collect_result(package_index=package_index)

def test_collect_result_raise(obj, caplog, monkeypatch):
    obj.open()

    #
    mock_gzip_open = mock.Mock()
    mock_gzip_open.side_effect = Exception()
    module = sys.modules['alphatwirl.concurrently.WorkingArea']
    monkeypatch.setattr(module.gzip, 'open', mock_gzip_open)

    #
    package_index = 9
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        ret = obj.collect_result(package_index=package_index)

    assert ret is None

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'WorkingArea' in caplog.records[0].name
    # assert 'No such file or directory' in caplog.records[0].msg

##__________________________________________________________________||
