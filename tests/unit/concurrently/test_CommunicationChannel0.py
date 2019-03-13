# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.concurrently import CommunicationChannel0

##__________________________________________________________________||
def task(*args, **kwargs):
    return

##__________________________________________________________________||
def test_one():
    obj = CommunicationChannel0()
    obj.begin()
    obj.put(task)
    obj.receive()
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('progressbar', [True, False])
def test_progressbar_deprecated(progressbar, caplog):
    with caplog.at_level(logging.WARNING):
        obj = CommunicationChannel0(progressbar=progressbar)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'CommunicationChannel0' in caplog.records[0].name
    assert 'deprecated.' in caplog.records[0].msg

##__________________________________________________________________||
