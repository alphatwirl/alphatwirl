# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

from alphatwirl.configure import build_progressMonitor_communicationChannel

##__________________________________________________________________||
def test_build_depricated(caplog):
    with pytest.raises(RuntimeError):
        with caplog.at_level(logging.ERROR):
            ret = build_progressMonitor_communicationChannel(quiet=True, processes=4)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    assert 'alphatwirl.configure' in caplog.records[0].name
    assert 'removed' in caplog.records[0].msg

##__________________________________________________________________||
