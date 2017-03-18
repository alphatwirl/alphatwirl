from alphatwirl.progressbar import ProgressReportPickup
import unittest
import multiprocessing

##__________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)
    def nreports(self): return 0

##__________________________________________________________________||
class MockReport(object): pass

##__________________________________________________________________||
class TestProgressReportPickup(unittest.TestCase):

    def test_start_join(self):
        queue = multiprocessing.Queue()
        presentation = MockPresentation()
        pickup = ProgressReportPickup(queue, presentation)
        pickup.start()
        queue.put(None)
        pickup.join()

##__________________________________________________________________||
