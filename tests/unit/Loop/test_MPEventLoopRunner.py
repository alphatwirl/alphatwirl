from alphatwirl.loop import MPEventLoopRunner
import unittest
import os

##__________________________________________________________________||
class MockCommunicationChannel(object):
    def __init__(self):
        self.eventLoops = [ ]
        self.resultsToReceive = [ ]

    def put(self, task):
        eventLoop = task
        self.eventLoops.append(eventLoop)

    def receive(self):
        return self.resultsToReceive

##__________________________________________________________________||
class MockResult(object): pass

##__________________________________________________________________||
class MockEventLoop(object): pass

##__________________________________________________________________||
class TestMPEventLoopRunner(unittest.TestCase):

    def test_repr(self):
        communicationChannel = MockCommunicationChannel()
        obj = MPEventLoopRunner(communicationChannel)
        repr(obj)

    def test_begin_end(self):
        communicationChannel = MockCommunicationChannel()
        obj = MPEventLoopRunner(communicationChannel)
        obj.begin()
        obj.end()

    def test_bgin_run_end(self):
        communicationChannel = MockCommunicationChannel()
        obj = MPEventLoopRunner(communicationChannel)
        obj.begin()

        eventLoop1 = MockEventLoop()
        obj.run(eventLoop1)

        eventLoop2 = MockEventLoop()
        obj.run(eventLoop2)

        self.assertEqual([eventLoop1, eventLoop2], communicationChannel.eventLoops)

        result1 = MockResult()
        result2 = MockResult()
        communicationChannel.resultsToReceive = [result1, result2]

        self.assertEqual([result1, result2], obj.end())

    # @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_wrong_number_or_results(self):
        communicationChannel = MockCommunicationChannel()
        obj = MPEventLoopRunner(communicationChannel)
        obj.begin()

        eventLoop1 = MockEventLoop()
        obj.run(eventLoop1)

        eventLoop2 = MockEventLoop()
        obj.run(eventLoop2)

        self.assertEqual([eventLoop1, eventLoop2], communicationChannel.eventLoops)

        result1 = MockResult()
        result2 = MockResult()
        communicationChannel.resultsToReceive = [result1]

        self.assertEqual([result1], obj.end())

##__________________________________________________________________||
