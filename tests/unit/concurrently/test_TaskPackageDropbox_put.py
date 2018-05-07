# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import TaskPackageDropbox

##__________________________________________________________________||
@pytest.fixture()
def workingarea():
    return mock.MagicMock()

@pytest.fixture()
def dispatcher():
    return mock.MagicMock()

@pytest.fixture()
def obj(workingarea, dispatcher):
    ret = TaskPackageDropbox(workingArea=workingarea, dispatcher=dispatcher, sleep=0.01)
    ret.open()
    yield ret
    ret.close()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_open_terminate_close(workingarea, dispatcher):

    obj = TaskPackageDropbox(workingArea=workingarea, dispatcher=dispatcher, sleep=0.01)

    assert 0 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 0 == dispatcher.terminate.call_count

    obj.open()
    assert 1 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 0 == dispatcher.terminate.call_count

    obj.terminate()
    assert 1 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 1 == dispatcher.terminate.call_count

    obj.close()
    assert 1 == workingarea.open.call_count
    assert 1 == workingarea.close.call_count
    assert 1 == dispatcher.terminate.call_count

def test_put(obj, workingarea, dispatcher):

    workingarea.put_package.side_effect = [0, 1] # pkgidx
    dispatcher.run.side_effect = [1001, 1002] # runid

    package0 = mock.MagicMock(name='package0')
    package1 = mock.MagicMock(name='package1')

    assert 0 == obj.put(package0)
    assert 1 == obj.put(package1)

    assert [mock.call(package0), mock.call(package1)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, 0), mock.call(workingarea, 1)] == dispatcher.run.call_args_list

def test_put_multiple(obj, workingarea, dispatcher):

    workingarea.put_package.side_effect = [0, 1] # pkgidx
    dispatcher.run_multiple.return_value = [1001, 1002] # runid

    package0 = mock.MagicMock(name='package0')
    package1 = mock.MagicMock(name='package1')

    assert [0, 1] == obj.put_multiple([package0, package1])

    assert [mock.call(package0), mock.call(package1)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, [0, 1])] == dispatcher.run_multiple.call_args_list

##__________________________________________________________________||
