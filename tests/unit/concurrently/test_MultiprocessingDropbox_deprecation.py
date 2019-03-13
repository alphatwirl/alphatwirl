# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import MultiprocessingDropbox

##__________________________________________________________________||
@pytest.mark.parametrize('progressbar', [True, False])
def test_progressbar_deprecated(progressbar, caplog):
    with caplog.at_level(logging.WARNING):
        obj = MultiprocessingDropbox(progressbar=progressbar)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    # assert 'MultiprocessingDropbox' in caplog.records[0].name # this becomes `alphatwirl.misc.deprecation`
    assert 'deprecated.' in caplog.records[0].msg

@pytest.fixture()
def mock_progressmonitor():
    ret = mock.Mock()
    return ret

def test_progressMonitor_deprecated(mock_progressmonitor, caplog):
    with caplog.at_level(logging.WARNING):
        obj = MultiprocessingDropbox(progressMonitor=mock_progressmonitor)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'MultiprocessingDropbox' in caplog.records[0].name
    assert 'deprecated.' in caplog.records[0].msg

##__________________________________________________________________||
