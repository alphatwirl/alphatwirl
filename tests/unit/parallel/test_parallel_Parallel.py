# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.parallel import Parallel

##__________________________________________________________________||
@pytest.fixture()
def progressMonitor():
    return mock.Mock()

@pytest.fixture()
def communicationChannel():
    return mock.Mock()

@pytest.fixture()
def workingarea():
    return mock.Mock()

@pytest.fixture()
def obj(progressMonitor, communicationChannel, workingarea):
    return Parallel(
        progressMonitor = progressMonitor,
        communicationChannel = communicationChannel,
        workingarea = workingarea
    )

def test_repr(obj):
    repr(obj)

def test_workingarea(obj, workingarea):
    assert workingarea is obj.workingarea

def test_begin_terminate_end(obj, progressMonitor, communicationChannel):

    obj.begin()
    assert [mock.call()] == progressMonitor.begin.call_args_list
    assert [mock.call()] == communicationChannel.begin.call_args_list

    obj.terminate()
    assert [mock.call()] == communicationChannel.terminate.call_args_list

    obj.end()
    assert [mock.call()] == progressMonitor.end.call_args_list
    assert [mock.call()] == communicationChannel.end.call_args_list

##__________________________________________________________________||
