from AlphaTwirl.EventReader import MPEventLoopRunner
from AlphaTwirl.Concurrently import CommunicationChannel
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
    def __init__(self, reader):
        self.reader = reader

    def __call__(self, progressReporter):
        self.reader._results = 3456
        return self.reader

##____________________________________________________________________________||
class MockEventLoopForProgressReporterTest(object):
    def __init__(self, reader):
        self.reader = reader

    def __call__(self, progressReporter):
        self.reader._results = [3456, progressReporter]
        return self.reader

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
        communicationChannel = CommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        communicationChannel.begin()
        runner.begin()
        runner.end()
        communicationChannel.end()

    def test_run(self):
        communicationChannel = CommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        communicationChannel.begin()
        runner.begin()

        reader = MockReader()
        eventLoop = MockEventLoop(reader)
        runner.run(eventLoop)


        self.assertIsNone(reader._results)

        runner.end()

        self.assertEqual(3456, reader._results)

        communicationChannel.end()

    def test_ProgressMonitor(self):
        progressMonitor = MockProgressMonitor()
        communicationChannel = CommunicationChannel(nprocesses = 3, progressMonitor = progressMonitor)
        runner = MPEventLoopRunner(communicationChannel)
        communicationChannel.begin()
        runner.begin()

        reader = MockReader()
        eventLoop = MockEventLoopForProgressReporterTest(reader)
        runner.run(eventLoop)

        self.assertIsNone(reader._results)

        runner.end()

        self.assertEqual(3456, reader._results[0])

        # assert that the EventLoop received a ProgressReporter
        self.assertIsInstance(reader._results[1], MockProgressReporter)

        communicationChannel.end()

##____________________________________________________________________________||
