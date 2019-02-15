# Tai Sakuma <tai.sakuma@gmail.com>
import logging

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.parallel import Parallel

##__________________________________________________________________||
@pytest.fixture()
def communicationChannel():
    return mock.Mock()

@pytest.fixture()
def workingarea():
    return mock.Mock()

@pytest.fixture()
def obj(communicationChannel, workingarea):
    return Parallel(
        progressMonitor=None,
        communicationChannel=communicationChannel,
        workingarea=workingarea
    )

def test_repr(obj):
    repr(obj)

def test_workingarea(obj, workingarea):
    assert workingarea is obj.workingarea

def test_begin_terminate_end(obj, communicationChannel):

    obj.begin()
    assert [mock.call()] == communicationChannel.begin.call_args_list

    obj.terminate()
    assert [mock.call()] == communicationChannel.terminate.call_args_list

    obj.end()
    assert [mock.call()] == communicationChannel.end.call_args_list

##__________________________________________________________________||
def test_deprectated(caplog):
    with caplog.at_level(logging.WARNING):
        Parallel(mock.Mock(), mock.Mock(), mock.Mock())

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'parallel' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
