# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import BProgressMonitor, ProgressReporter, ProgressReport

import alphatwirl

##__________________________________________________________________||
@pytest.fixture()
def presentation():
    ret = mock.MagicMock()
    return ret

@pytest.fixture()
def monitor(presentation):
    return BProgressMonitor(presentation)


##__________________________________________________________________||
def test_repr(monitor):
    repr(monitor)

def test_begin_end(monitor, presentation):
    presentation.nreports.return_value = 0
    monitor.begin()
    assert isinstance(alphatwirl.progressbar._progress_reporter, ProgressReporter)
    monitor.end()
    assert alphatwirl.progressbar._progress_reporter is None

def test_createReporter(monitor):
    reporter = monitor.createReporter()
    assert isinstance(reporter, ProgressReporter)

def test_send_report(monitor, presentation):
    presentation.nreports.return_value = 10
    monitor.begin()
    reporter = monitor.createReporter()
    report = ProgressReport('task1', 0, 3)
    reporter.report(report)
    monitor.end()

##__________________________________________________________________||
