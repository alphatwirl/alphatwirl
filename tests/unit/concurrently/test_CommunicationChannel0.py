# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel0

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mock_atpbar(monkeypatch):
    ret = mock.Mock()
    ret.funcs._do_not_start_pickup = False
    module = sys.modules['alphatwirl.concurrently.CommunicationChannel0']
    monkeypatch.setattr(module, 'atpbar', ret)
    return ret

##__________________________________________________________________||
def task(*args, **kwargs):
    return

##__________________________________________________________________||
def test_progressbar_on(mock_atpbar):
    obj = CommunicationChannel0(progressbar=True)
    obj.begin()
    obj.put(task)
    obj.receive()
    obj.end()
    assert mock_atpbar.funcs._do_not_start_pickup is False


def test_progressbar_off(mock_atpbar):
    obj = CommunicationChannel0(progressbar=False)
    obj.begin()
    obj.put(task)
    obj.receive()
    obj.end()
    assert mock_atpbar.funcs._do_not_start_pickup is True


##__________________________________________________________________||
