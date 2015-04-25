from AlphaTwirl.EventReader import MPEventLoopRunner
import unittest
import os

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self._results = None

    def setResults(self, results):
        self._results = results

    def results(self):
        return self._results

##____________________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, readers):
        self.readers = readers

    def __call__(self, progressReporter):
        for reader in self.readers:
            reader._results = 3456
        return self.readers

##____________________________________________________________________________||
class MockEventLoopForProgressReporterTest(object):
    def __init__(self, readers):
        self.readers = readers

    def __call__(self, progressReporter):
        for reader in self.readers:
            reader._results = [3456, progressReporter]
        return self.readers

##____________________________________________________________________________||
class MockProgressReporter(object):
    def report(self, event, component): pass

##____________________________________________________________________________||
class MockProgressMonitor(object):
    def createReporter(self): return MockProgressReporter()
    def addWorker(self, worker): pass
    def monitor(self): pass
    def last(self): pass

##____________________________________________________________________________||
class TestMPEventLoopRunner(unittest.TestCase):

    def test_begin_end(self):
        runner = MPEventLoopRunner()
        runner.begin()
        runner.end()

    def test_run(self):
        runner = MPEventLoopRunner()
        runner.begin()

        reader1 = MockReader()
        reader2 = MockReader()
        eventLoop = MockEventLoop([reader1, reader2])
        runner.run(eventLoop)

        self.assertIsNone(reader1._results)
        self.assertIsNone(reader2._results)

        runner.end()

        self.assertEqual(3456, reader1._results)
        self.assertEqual(3456, reader2._results)

    def test_ProgressMonitor(self):
        progressMonitor = MockProgressMonitor()
        runner = MPEventLoopRunner(nprocesses = 3, progressMonitor = progressMonitor)
        runner.begin()

        reader1 = MockReader()
        reader2 = MockReader()
        eventLoop = MockEventLoopForProgressReporterTest([reader1, reader2])
        runner.run(eventLoop)

        self.assertIsNone(reader1._results)
        self.assertIsNone(reader2._results)

        runner.end()

        self.assertEqual(3456, reader1._results[0])
        self.assertEqual(3456, reader2._results[0])

        # assert that the EventLoop received a ProgressReporter
        self.assertIsInstance(reader1._results[1], MockProgressReporter)
        self.assertIsInstance(reader2._results[1], MockProgressReporter)

##____________________________________________________________________________||
