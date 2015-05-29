from AlphaTwirl.Concurrently import CommunicationChannel
import unittest
import time
import os

##__________________________________________________________________||
class MockResult(object):
    def __init__(self, data = None):
        self.data = data

##__________________________________________________________________||
class MockTask(object):
    def __init__(self, result, time):
        self.result = result
        self.time = time

    def __call__(self, progressReporter):
        time.sleep(self.time)
        self.result.progressReporter = progressReporter
        return self.result

##__________________________________________________________________||
class MockProgressReporter(object):
    def report(self, event, component): pass

##__________________________________________________________________||
class MockProgressMonitor(object):
    def createReporter(self): return MockProgressReporter()
    def monitor(self): pass
    def last(self): pass

##__________________________________________________________________||
class TestCommunicationChannel(unittest.TestCase):

    def test_begin_end(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()
        communicationChannel.end()

    def test_put(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        communicationChannel.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        communicationChannel.put(task2)

        communicationChannel.end()

    def test_receive(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        communicationChannel.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        communicationChannel.put(task2)

        actual = [r.data for r in communicationChannel.receive()]
        self.assertEqual(set(['task1', 'task2']), set(actual))

        communicationChannel.end()

    def test_receive_without_put(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()

        self.assertEqual([ ], communicationChannel.receive())

        communicationChannel.end()

    def test_ProgressMonitor(self):
        progressMonitor = MockProgressMonitor()
        communicationChannel = CommunicationChannel(nprocesses = 3, progressMonitor = progressMonitor)
        communicationChannel.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        communicationChannel.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        communicationChannel.put(task2)

        # the results in the main process don't have a ProgressReporter
        self.assertFalse(hasattr(result1, "progressReporter"))
        self.assertFalse(hasattr(result2, "progressReporter"))

        # the results returned from other processes do.
        returnedResults = communicationChannel.receive()
        self.assertIsInstance(returnedResults[0].progressReporter, MockProgressReporter)
        self.assertIsInstance(returnedResults[1].progressReporter, MockProgressReporter)

        communicationChannel.end()

    def test_receive_order(self):
        # test the order of results
        pass

##__________________________________________________________________||
