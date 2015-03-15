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
class MockPresentationForTestLast(object):
    def __init__(self): self._nreports = 0
    def present(self, report): self._nreports -= 1
    def nreports(self): return self._nreports

##____________________________________________________________________________||
class MockPresentForTestMonitor(object):
    def __init__(self): self.called = False
    def __call__(self): self.called = True
    def reset(self): self.called = False

##____________________________________________________________________________||
class MockPresentForTestLast(object):
    def __init__(self, presentation):
        self.presentation = presentation
        self.called = False
    def __call__(self):
        self.presentation.present(MockReport())
        self.called = True
    def reset(self): self.called = False

##____________________________________________________________________________||
class MockPresentForTestLastWaitTime(object):
    def __init__(self, presentation):
        self.presentation = presentation
        self.called = False
    def __call__(self):
        # self.presentation.present(MockReport()) # never present
        self.called = True
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

        mockpresent = MockPresentForTestMonitor()
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

    def test_last_no_reports(self):
        presentation = MockPresentationForTestLast()
        monitor = MPProgressMonitor(presentation)

        mockpresent = MockPresentForTestLast(presentation)
        monitor._present = mockpresent

        self.assertFalse(mockpresent.called)

        self.assertEqual(0, presentation._nreports)
        monitor.last()

        self.assertFalse(mockpresent.called)
        self.assertEqual(0, presentation._nreports)

    def test_last_with_reports(self):
        presentation = MockPresentationForTestLast()
        presentation._nreports = 3
        monitor = MPProgressMonitor(presentation)

        mockpresent = MockPresentForTestLast(presentation)
        monitor._present = mockpresent

        self.assertFalse(mockpresent.called)

        self.assertEqual(3, presentation._nreports)
        monitor.last()

        self.assertTrue(mockpresent.called)
        self.assertEqual(0, presentation._nreports)

    def test_last_waittime(self):
        presentation = MockPresentationForTestLast()
        presentation._nreports = 3
        monitor = MPProgressMonitor(presentation)
        monitor.lastWaitTime = 0.05

        mockpresent = MockPresentForTestLastWaitTime(presentation)
        monitor._present = mockpresent

        self.assertFalse(mockpresent.called)

        self.assertEqual(3, presentation._nreports)
        monitor.last()

        self.assertTrue(mockpresent.called)
        self.assertEqual(3, presentation._nreports)

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
