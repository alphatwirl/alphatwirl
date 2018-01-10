# Tai Sakuma <tai.sakuma@gmail.com>
import sys

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import Queue, ProgressMonitor

##__________________________________________________________________||
def test_queue_put():
    presentation = mock.MagicMock()
    queue = Queue(presentation)
    report = mock.MagicMock()
    queue.put(report)
    presentation.present.assert_called_once_with(report)

##__________________________________________________________________||
def test_begin_end():
    presentation = mock.MagicMock()
    monitor = ProgressMonitor(presentation)
    monitor.begin()
    monitor.end()

def test_createReporter(monkeypatch):
    module = sys.modules['alphatwirl.progressbar.ProgressMonitor']
    mock_reporter = mock.MagicMock()
    MockReporter = mock.MagicMock()
    MockReporter.return_value = mock_reporter
    monkeypatch.setattr(module, 'ProgressReporter', MockReporter)

    presentation = mock.MagicMock()
    monitor = ProgressMonitor(presentation)
    assert monitor.createReporter() is mock_reporter
    MockReporter.assert_called_once_with(monitor.queue)

##__________________________________________________________________||
