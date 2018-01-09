# Tai Sakuma <tai.sakuma@gmail.com>

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReporter, Queue, ProgressMonitor

##__________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)

##__________________________________________________________________||
class MockReport(object): pass

##__________________________________________________________________||
def test_queue_put():
    presentation = MockPresentation()
    queue = Queue(presentation)
    report = MockReport()
    queue.put(report)
    assert [report, ] == presentation.reports

##__________________________________________________________________||
def test_begin_end():
    presentation = MockPresentation()
    monitor = ProgressMonitor(presentation)
    monitor.begin()
    monitor.end()

def test_createReporter():
    presentation = MockPresentation()
    monitor = ProgressMonitor(presentation)
    assert isinstance(monitor.createReporter(), ProgressReporter)

##__________________________________________________________________||
