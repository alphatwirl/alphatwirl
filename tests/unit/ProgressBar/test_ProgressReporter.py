from AlphaTwirl.ProgressBar import ProgressReporter, ProgressReport
import unittest

##__________________________________________________________________||
class MockTime(object):
    def __init__(self, time): self.time = time
    def __call__(self): return self.time

##__________________________________________________________________||
class MockQueue(object):
    def __init__(self): self.queue = [ ]
    def put(self, report): self.queue.append(report)
    def get(self): return self.queue.pop(0)
    def empty(self): return len(self.queue) == 0

##__________________________________________________________________||
class TestProgressReporter(unittest.TestCase):

    def test_report(self):
        queue = MockQueue()
        reporter = ProgressReporter(queue)

        mocktime = MockTime(1000.0)
        reporter._time = mocktime

        reporter._readTime()
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.2
        reporter._report(ProgressReport(name = "dataset1", done = 124, total = 1552))

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
        report = ProgressReport(name = "dataset1", done = 124, total = 1552)
        self.assertFalse(reporter._needToReport(report))
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.03
        report = ProgressReport(name = "dataset1", done = 124, total = 1552)
        self.assertTrue(reporter._needToReport(report))
        self.assertEqual(1000.0, reporter.lastTime)

        mocktime.time = 1000.03
        report = ProgressReport(name = "dataset1", done = 1552, total = 1552)
        self.assertTrue(reporter._needToReport(report))

##__________________________________________________________________||
