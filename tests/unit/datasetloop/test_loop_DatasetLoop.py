# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.datasetloop import DatasetLoop

##__________________________________________________________________||
@pytest.fixture()
def reader():
    return mock.Mock()

@pytest.fixture()
def datasets():
    dataset1 = mock.Mock()
    dataset2 = mock.Mock()
    return [dataset1, dataset2]

@pytest.fixture()
def obj(datasets, reader):
    return DatasetLoop(datasets, reader)

def test_repr(obj):
    repr(obj)

def test_call(obj, reader, datasets):
    result = obj()
    assert [mock.call()] == reader.begin.call_args_list
    assert [mock.call(c) for c in datasets] == reader.read.call_args_list
    assert reader.end() is result

##__________________________________________________________________||
