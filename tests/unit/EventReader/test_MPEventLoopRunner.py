from AlphaTwirl.EventReader import MPEventLoopRunner
import unittest
import os

##__________________________________________________________________||
class MockCommunicationChannel(object):
    def __init__(self):
        self.eventLoops = [ ]
        self.readersToReceive = [ ]

    def put(self, task):
        eventLoop = task
        self.eventLoops.append(eventLoop)

    def receive(self):
        return self.readersToReceive

##__________________________________________________________________||
class MockResult(object): pass

##__________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self._result = None
        self._isSetResultsCalled = False

    def setResults(self, result):
        self._result = result
        self._isSetResultsCalled = True

    def results(self):
        return self._result

##__________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, reader):
        self.reader = reader

##__________________________________________________________________||
class TestMPEventLoopRunner(unittest.TestCase):

    def test_begin_end(self):
        communicationChannel = MockCommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        runner.begin()
        runner.end()

    def test_run(self):
        communicationChannel = MockCommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        runner.begin()

        reader1 = MockReader()
        eventLoop1 = MockEventLoop(reader1)
        runner.run(eventLoop1)

        reader2 = MockReader()
        eventLoop2 = MockEventLoop(reader2)
        runner.run(eventLoop2)

        self.assertEqual([eventLoop1, eventLoop2], communicationChannel.eventLoops)

    def test_run_end_same_readers(self):
        communicationChannel = MockCommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        runner.begin()

        reader1 = MockReader()
        eventLoop1 = MockEventLoop(reader1)
        runner.run(eventLoop1)

        reader2 = MockReader()
        eventLoop2 = MockEventLoop(reader2)
        runner.run(eventLoop2)

        communicationChannel.readersToReceive = [reader1, reader2]

        runner.end()
        self.assertFalse(reader1._isSetResultsCalled)
        self.assertFalse(reader2._isSetResultsCalled)

    def test_run_end_different_readers(self):
        communicationChannel = MockCommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        runner.begin()

        reader1 = MockReader()
        eventLoop1 = MockEventLoop(reader1)
        runner.run(eventLoop1)

        reader2 = MockReader()
        eventLoop2 = MockEventLoop(reader2)
        runner.run(eventLoop2)

        reader3 = MockReader()
        reader4 = MockReader()
        reader3._result = MockResult()
        reader4._result = MockResult()
        communicationChannel.readersToReceive = [reader3, reader4]

        runner.end()
        self.assertTrue(reader1._isSetResultsCalled)
        self.assertTrue(reader2._isSetResultsCalled)

        self.assertEqual(reader3._result, reader1._result)
        self.assertEqual(reader4._result, reader2._result)

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_run_end_wrong_number_or_readers(self):
        communicationChannel = MockCommunicationChannel()
        runner = MPEventLoopRunner(communicationChannel)
        runner.begin()

        reader1 = MockReader()
        eventLoop1 = MockEventLoop(reader1)
        runner.run(eventLoop1)

        reader2 = MockReader()
        eventLoop2 = MockEventLoop(reader2)
        runner.run(eventLoop2)

        communicationChannel.readersToReceive = [ ]

        runner.end()

##__________________________________________________________________||
