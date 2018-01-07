# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import time
import multiprocessing

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReportPickup

##__________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)
    def nreports(self): return 0

@pytest.fixture()
def presentation():
    return MockPresentation()

@pytest.fixture()
def queue():
    return multiprocessing.Queue()

@pytest.fixture()
def pickup(queue, presentation):
    return ProgressReportPickup(queue, presentation)

##__________________________________________________________________||
class MockReport(object): pass

##__________________________________________________________________||
def test_start_join(pickup, queue, presentation):
    pickup.start()
    queue.put(None)
    pickup.join()

##__________________________________________________________________||
