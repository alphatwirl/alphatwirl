from alphatwirl.concurrently import CommunicationChannel0
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
class TestCommunicationChannel0(unittest.TestCase):

    def test_begin_end(self):
        communicationChannel = CommunicationChannel0()
        communicationChannel.begin()
        communicationChannel.end()

    def test_begin_twice(self):
        communicationChannel = CommunicationChannel0()
        communicationChannel.begin()
        communicationChannel.begin()
        communicationChannel.end()

    def test_put(self):
        communicationChannel = CommunicationChannel0()
        communicationChannel.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        communicationChannel.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        communicationChannel.put(task2)

        communicationChannel.end()

    def test_put_receive(self):
        communicationChannel = CommunicationChannel0()
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

        communicationChannel = CommunicationChannel0()
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
        communicationChannel = CommunicationChannel0()
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
        communicationChannel = CommunicationChannel0()
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
        communicationChannel = CommunicationChannel0()
        communicationChannel.begin()

        self.assertEqual([ ], communicationChannel.receive())

        communicationChannel.end()


##__________________________________________________________________||
