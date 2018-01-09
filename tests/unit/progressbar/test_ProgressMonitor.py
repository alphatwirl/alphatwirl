# Tai Sakuma <tai.sakuma@gmail.com>

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReporter, Queue, ProgressMonitor

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

def test_createReporter():
    presentation = mock.MagicMock()
    monitor = ProgressMonitor(presentation)
    assert isinstance(monitor.createReporter(), ProgressReporter)

##__________________________________________________________________||
