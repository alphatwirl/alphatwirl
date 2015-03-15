from AlphaTwirl.ProgressBar import ProgressReporter
import unittest

##____________________________________________________________________________||
class MockTime(object):
    def __init__(self, time): self.time = time
    def __call__(self): return self.time

##____________________________________________________________________________||
class MockReport(object): pass

##____________________________________________________________________________||
class MockEvent(object):
    def __init__(self):
        self.iEvent = 123
        self.nEvents = 1552

##____________________________________________________________________________||
class MockComponent(object):
    def __init__(self): self.name = "dataset1"

##____________________________________________________________________________||
class MockQueue(object):
    def __init__(self): self.queue = [ ]
    def put(self, report): self.queue.append(report)
    def get(self): return self.queue.pop(0)
    def empty(self): return len(self.queue) == 0

##____________________________________________________________________________||
class TestMPProgressMonitor(unittest.TestCase):

    def test_report(self):
        queue = MockQueue()
        reporter = ProgressReporter(queue)

        mocktime = MockTime(1000.0)
        reporter._time = mocktime

        reporter._readTime()
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.2
        event = MockEvent()
        component = MockComponent()
        reporter._report(event, component)

        report = queue.get()
        self.assertEqual("dataset1", report.name)
        self.assertEqual(124, report.done)
        self.assertEqual(1552, report.total)

        self.assertEqual(1000.2, reporter.lastTime)

    def test_needToReport(self):
        queue = MockQueue()
        reporter = ProgressReporter(queue)

        mocktime = MockTime(1000.0)
        reporter._time = mocktime

        reporter._readTime()
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.01
        event = MockEvent()
        component = MockComponent()
        self.assertFalse(reporter.needToReport(event, component))
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.03
        event = MockEvent()
        component = MockComponent()
        self.assertTrue(reporter.needToReport(event, component))
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.03
        event = MockEvent()
        event.iEvent = 1551 # = event.nEvents - 1
        component = MockComponent()
        self.assertTrue(reporter.needToReport(event, component))

##____________________________________________________________________________||
