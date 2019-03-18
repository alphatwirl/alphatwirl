# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import TaskPackageDropbox
from alphatwirl.concurrently import WorkingArea, HTCondorJobSubmitter

##__________________________________________________________________||
@pytest.fixture()
def mock_workingarea():
    ret = mock.Mock(spec=WorkingArea)
    return ret

@pytest.fixture()
def mock_dispatcher():
    ret = mock.Mock(spec=HTCondorJobSubmitter)
    return ret

@pytest.fixture()
def obj(mock_workingarea, mock_dispatcher):
    ret = TaskPackageDropbox(workingArea=mock_workingarea, dispatcher=mock_dispatcher, sleep=0.01)
    ret.open()
    yield ret
    ret.close()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_open_terminate_close(mock_workingarea, mock_dispatcher):

    obj = TaskPackageDropbox(workingArea=mock_workingarea, dispatcher=mock_dispatcher, sleep=0.01)

    assert 0 == mock_workingarea.open.call_count
    assert 0 == mock_workingarea.close.call_count
    assert 0 == mock_dispatcher.terminate.call_count

    obj.open()
    assert 1 == mock_workingarea.open.call_count
    assert 0 == mock_workingarea.close.call_count
    assert 0 == mock_dispatcher.terminate.call_count

    obj.terminate()
    assert 1 == mock_workingarea.open.call_count
    assert 0 == mock_workingarea.close.call_count
    assert 1 == mock_dispatcher.terminate.call_count

    obj.close()
    assert 1 == mock_workingarea.open.call_count
    assert 1 == mock_workingarea.close.call_count
    assert 1 == mock_dispatcher.terminate.call_count

def test_put(obj, mock_workingarea, mock_dispatcher):

    mock_workingarea.put_package.side_effect = [0, 1] # pkgidx
    mock_dispatcher.run.side_effect = [1001, 1002] # runid

    package0 = mock.Mock(name='package0')
    package1 = mock.Mock(name='package1')

    assert 0 == obj.put(package0)
    assert 1 == obj.put(package1)

    assert [mock.call(package0), mock.call(package1)] == mock_workingarea.put_package.call_args_list
    assert [mock.call(mock_workingarea, 0), mock.call(mock_workingarea, 1)] == mock_dispatcher.run.call_args_list

def test_put_multiple(obj, mock_workingarea, mock_dispatcher):

    mock_workingarea.put_package.side_effect = [0, 1] # pkgidx
    mock_dispatcher.run_multiple.return_value = [1001, 1002] # runid

    package0 = mock.Mock(name='package0')
    package1 = mock.Mock(name='package1')

    assert [0, 1] == obj.put_multiple([package0, package1])

    assert [mock.call(package0), mock.call(package1)] == mock_workingarea.put_package.call_args_list
    assert [mock.call(mock_workingarea, [0, 1])] == mock_dispatcher.run_multiple.call_args_list

##__________________________________________________________________||
