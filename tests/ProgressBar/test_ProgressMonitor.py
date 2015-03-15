from AlphaTwirl.ProgressBar import ProgressReporter, Queue, ProgressMonitor, MPProgressMonitor
import unittest

##____________________________________________________________________________||
class MockTime(object):
    def __init__(self, time): self.time = time
    def __call__(self): return self.time

##____________________________________________________________________________||
class MockPresentation(object):
    def __init__(self): self.reports = [ ]
    def present(self, report): self.reports.append(report)

##____________________________________________________________________________||
class MockPresent(object):
    def __init__(self): self.called = False
    def __call__(self): self.called = True
    def reset(self): self.called = False

##____________________________________________________________________________||
class MockReport(object): pass

##____________________________________________________________________________||
class MockQueue(object):
    def __init__(self): self.queue = [ ]
    def put(self, report): self.queue.append(report)
    def get(self): return self.queue.pop(0)
    def empty(self): return len(self.queue) == 0

##____________________________________________________________________________||
class TestQueue(unittest.TestCase):

    def test_put(self):
        presentation = MockPresentation()
        queue = Queue(presentation)
        report = MockReport()
        queue.put(report)
        self.assertEqual([report, ], presentation.reports)

##____________________________________________________________________________||
class TestProgressMonitor(unittest.TestCase):

    def test_monitor(self):
        presentation = MockPresentation()
        monitor = ProgressMonitor(presentation)
        monitor.monitor()

    def test_createReporter(self):
        presentation = MockPresentation()
        monitor = ProgressMonitor(presentation)
        self.assertIsInstance(monitor.createReporter(), ProgressReporter)

##____________________________________________________________________________||
class TestMPProgressMonitor(unittest.TestCase):

    def test_monitor(self):
        presentation = MockPresentation()
        monitor = MPProgressMonitor(presentation)

        mocktime = MockTime(1000.0)
        monitor._time = mocktime

        mockpresent = MockPresent()
        monitor._present = mockpresent

        monitor._readTime()
        self.assertEqual(1000.0, monitor.lastTime)

        self.assertFalse(mockpresent.called)

        # after the interval
        mocktime.time = 1000.2
        monitor.monitor()

        self.assertEqual(1000.2, monitor.lastTime)
        self.assertTrue(mockpresent.called)

        mockpresent.reset()
        self.assertFalse(mockpresent.called)

        # within the interval
        mocktime.time = 1000.23
        monitor.monitor()

        self.assertEqual(1000.2, monitor.lastTime)
        self.assertFalse(mockpresent.called)

        mockpresent.reset()
        self.assertFalse(mockpresent.called)

        # after the interval
        mocktime.time = 1000.38
        monitor.monitor()

        self.assertEqual(1000.38, monitor.lastTime)
        self.assertTrue(mockpresent.called)

    def test_last(self):
        presentation = MockPresentation()
        monitor = MPProgressMonitor(presentation)

        mockpresent = MockPresent()
        monitor._present = mockpresent

        self.assertFalse(mockpresent.called)

        monitor.last()

        self.assertTrue(mockpresent.called)

    def test_present(self):
        queue = MockQueue()
        presentation = MockPresentation()
        monitor = MPProgressMonitor(presentation)
        monitor.queue = queue

        report1 = MockReport()
        queue.put(report1)
        report2 = MockReport()
        queue.put(report2)
        report3 = MockReport()
        queue.put(report3)
        self.assertEqual([report1, report2, report3], queue.queue)

        monitor._present()

        self.assertEqual([report1, report2, report3], presentation.reports)
        self.assertEqual([ ], queue.queue)

    def test_createReporter(self):
        presentation = MockPresentation()
        monitor = MPProgressMonitor(presentation)
        self.assertIsInstance(monitor.createReporter(), ProgressReporter)

##____________________________________________________________________________||
