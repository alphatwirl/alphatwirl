from alphatwirl.progressbar import ProgressReporter, BProgressMonitor
import unittest

##__________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)
    def nreports(self): return 0

##__________________________________________________________________||
class MockReport(object): pass

##__________________________________________________________________||
class TestBProgressMonitor(unittest.TestCase):

    def test_repr(self):
        presentation = MockPresentation()
        monitor = BProgressMonitor(presentation)
        repr(monitor)

    def test_begin_end(self):
        presentation = MockPresentation()
        monitor = BProgressMonitor(presentation)
        monitor.begin()
        monitor.end()

    def test_createReporter(self):
        presentation = MockPresentation()
        monitor = BProgressMonitor(presentation)
        self.assertIsInstance(monitor.createReporter(), ProgressReporter)

##__________________________________________________________________||
