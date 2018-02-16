# Tai Sakuma <tai.sakuma@gmail.com>
import os
import gzip
import pytest

try:
    import cPickle as pickle
except:
    import pickle

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.datasetloop import ResumableDatasetLoop

##__________________________________________________________________||
class MockReader(object):
    def begin(self):
        pass

    def read(self, dataset):
        pass

    def end(self):
        pass

##__________________________________________________________________||

@pytest.fixture()
def reader():
    ret = MockReader()
    ret.original_id = id(ret)
    return ret

@pytest.fixture()
def datasets():
    dataset1 = mock.Mock()
    dataset2 = mock.Mock()
    return [dataset1, dataset2]

@pytest.fixture()
def workingarea(tmpdir_factory):
    ret = mock.Mock()
    ret.path = str(tmpdir_factory.mktemp(''))
    return ret

@pytest.fixture()
def obj(datasets, reader, workingarea):
    return ResumableDatasetLoop(datasets, reader, workingarea)

def test_repr(obj):
    repr(obj)

def test_call(obj, reader, workingarea):
    result = obj()
    path = os.path.join(workingarea.path, 'reader.p.gz')
    with gzip.open(path, 'rb') as f:
        reader_unpickled = pickle.load(f)
    assert reader.original_id == reader_unpickled.original_id

##__________________________________________________________________||
