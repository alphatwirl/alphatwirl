from alphatwirl.progressbar import ProgressReporter, ProgressReport
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

    def test_repr(self):
        queue = MockQueue()
        obj = ProgressReporter(queue)
        repr(obj)

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

        interval = reporter.interval
        self.assertEqual(0.1, interval)

        mocktime = MockTime(1000.0)
        reporter._time = mocktime

        reporter._readTime()
        self.assertEqual(1000.0, reporter.lastTime)

        # before the interval passes
        mocktime.time += 0.1*interval
        report = ProgressReport(name = "dataset1", done = 124, total = 1552)
        self.assertFalse(reporter._needToReport(report))
        self.assertEqual(1000.0, reporter.lastTime)

        # the last report before the interval passes
        report = ProgressReport(name = "dataset1", done = 1552, total = 1552)
        self.assertTrue(reporter._needToReport(report))
        self.assertEqual(1000.0, reporter.lastTime)

        # after the interval passes
        mocktime.time += 1.2*interval
        report = ProgressReport(name = "dataset2", done = 1022, total = 4000)
        self.assertTrue(reporter._needToReport(report))
        self.assertEqual(1000.0, reporter.lastTime)

##__________________________________________________________________||
