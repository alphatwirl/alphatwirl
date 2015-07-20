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

    def test_init(self):
        self.assertRaises(ValueError, CommunicationChannel, nprocesses = 0)

    def test_begin_end(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()
        communicationChannel.end()

    def test_begin_twice(self):
        nprocesses = 8
        communicationChannel = CommunicationChannel(nprocesses = nprocesses)
        communicationChannel.begin()
        self.assertEqual(nprocesses, communicationChannel.nCurrentProcesses)
        communicationChannel.begin()
        self.assertEqual(nprocesses, communicationChannel.nCurrentProcesses)
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

    def test_put_receive(self):
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

    def test_receive_order(self):
        # results of tasks are sorted in the order in which the tasks
        # are put.

        communicationChannel = CommunicationChannel()
        communicationChannel.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.010)
        communicationChannel.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        communicationChannel.put(task2)

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.005)
        communicationChannel.put(task3)

        actual = [r.data for r in communicationChannel.receive()]
        self.assertEqual(['task1', 'task2', 'task3'], actual)

        communicationChannel.end()

    def test_put_receive_repeat(self):
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

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.002)
        communicationChannel.put(task3)

        result4 = MockResult('task4')
        task4 = MockTask(result4, 0.002)
        communicationChannel.put(task4)

        actual = [r.data for r in communicationChannel.receive()]
        self.assertEqual(set(['task3', 'task4']), set(actual))

        communicationChannel.end()

    def test_begin_put_recive_end_repeat(self):
        communicationChannel = CommunicationChannel()
        communicationChannel.begin()

        result = MockResult('task1')
        task = MockTask(result, 0.003)
        communicationChannel.put(task)

        communicationChannel.receive()

        communicationChannel.end()

        communicationChannel.begin()

        result = MockResult('task2')
        task = MockTask(result, 0.003)
        communicationChannel.put(task)

        communicationChannel.receive()

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


##__________________________________________________________________||
