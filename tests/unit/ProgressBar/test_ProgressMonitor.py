from alphatwirl.progressbar import ProgressReporter, Queue, ProgressMonitor
import unittest

##__________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)

##__________________________________________________________________||
class MockReport(object): pass

##__________________________________________________________________||
class TestQueue(unittest.TestCase):

    def test_put(self):
        presentation = MockPresentation()
        queue = Queue(presentation)
        report = MockReport()
        queue.put(report)
        self.assertEqual([report, ], presentation.reports)

##__________________________________________________________________||
class TestProgressMonitor(unittest.TestCase):

    def test_begin_end(self):
        presentation = MockPresentation()
        monitor = ProgressMonitor(presentation)
        monitor.begin()
        monitor.end()

    def test_createReporter(self):
        presentation = MockPresentation()
        monitor = ProgressMonitor(presentation)
        self.assertIsInstance(monitor.createReporter(), ProgressReporter)

##__________________________________________________________________||
