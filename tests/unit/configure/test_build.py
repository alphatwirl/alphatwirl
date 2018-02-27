# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from alphatwirl.configure import build_progressMonitor_communicationChannel

##__________________________________________________________________||
def test_build_depricated(caplog):
    with caplog.at_level(logging.WARNING):
        ret = build_progressMonitor_communicationChannel(quiet=True, processes=4)

    progressMonitor, communicationChannel = ret
    assert 'NullProgressMonitor' == progressMonitor.__class__.__name__
    assert 'CommunicationChannel' == communicationChannel.__class__.__name__
    assert 'MultiprocessingDropbox' == communicationChannel.dropbox.__class__.__name__

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'alphatwirl.configure' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
