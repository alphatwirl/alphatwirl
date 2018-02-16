# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.datasetloop import DatasetLoop
from alphatwirl.datasetloop import ResumableDatasetLoop

##__________________________________________________________________||
@pytest.fixture()
def datasets():
    dataset1 = mock.Mock()
    dataset2 = mock.Mock()
    return [dataset1, dataset2]

@pytest.fixture()
def reader():
    return mock.Mock()

@pytest.fixture()
def workingarea(monkeypatch):
    module = sys.modules['alphatwirl.datasetloop.loop']
    monkeypatch.setattr(module, 'os', mock.Mock())
    monkeypatch.setattr(module, 'gzip', mock.MagicMock())
    monkeypatch.setattr(module, 'pickle', mock.Mock())
    return mock.Mock()

@pytest.fixture(
    params=[0, 1],
    ids=('DatasetLoop', 'ResumableDatasetLoop')
)
def obj(request, datasets, reader, workingarea):
    if request.param == 0:
        return DatasetLoop(datasets, reader)
    else:
        return ResumableDatasetLoop(datasets, reader, workingarea)

def test_repr(obj):
    repr(obj)

def test_call(obj, reader, datasets):
    result = obj()
    assert [mock.call()] == reader.begin.call_args_list
    assert [mock.call(c) for c in datasets] == reader.read.call_args_list
    assert reader.end() is result

##__________________________________________________________________||
