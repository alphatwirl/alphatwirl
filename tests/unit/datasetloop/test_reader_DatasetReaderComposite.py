# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.datasetloop import DatasetReaderComposite

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return DatasetReaderComposite()

def test_repr(obj):
    repr(obj)

def test_one(obj):
    reader1 = mock.Mock()
    reader2 = mock.Mock()

    dataset1 = mock.Mock()
    dataset2 = mock.Mock()

    obj.add(reader1)
    obj.add(reader2)

    obj.begin()

    assert [mock.call()] == reader1.begin.call_args_list
    assert [mock.call()] == reader2.begin.call_args_list

    obj.read(dataset1)
    obj.read(dataset2)

    assert [mock.call(dataset1), mock.call(dataset2)] == reader1.read.call_args_list
    assert [mock.call(dataset1), mock.call(dataset2)] == reader2.read.call_args_list

    results = obj.end()
    assert [reader1.end(), reader2.end()] == results

##__________________________________________________________________||
