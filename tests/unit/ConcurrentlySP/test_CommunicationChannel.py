import unittest
import time
import os
import tempfile
import shutil

from AlphaTwirl.ConcurrentlySP import CommunicationChannel

##__________________________________________________________________||
class MockTask(object):
    def __init__(self, result, time):
        self.result = result
        self.time = time

    def __call__(self):
        time.sleep(self.time)
        return self.result

##__________________________________________________________________||
class MockResult(object):
    def __init__(self, data = None):
        self.data = data

##__________________________________________________________________||
class TestCommunicationChannel(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_begin_end(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()
        obj.end()

    def test_begin_twice(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()
        obj.begin()
        obj.end()

    def test_put(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        obj.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        obj.put(task2)

        obj.end()

    def test_put_receive(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        obj.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        obj.put(task2)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task1', 'task2']), set(actual))

        obj.end()

    def test_receive_order(self):
        # results of tasks are sorted in the order in which the tasks
        # are put.

        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.010)
        obj.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        obj.put(task2)

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.005)
        obj.put(task3)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(['task1', 'task2', 'task3'], actual)

        obj.end()

    def test_put_receive_repeat(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        obj.put(task1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        obj.put(task2)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task1', 'task2']), set(actual))

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.002)
        obj.put(task3)

        result4 = MockResult('task4')
        task4 = MockTask(result4, 0.002)
        obj.put(task4)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task3', 'task4']), set(actual))

        obj.end()

    def test_begin_put_recive_end_repeat(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        result = MockResult('task1')
        task = MockTask(result, 0.003)
        obj.put(task)

        obj.receive()

        obj.end()

        obj.begin()

        result = MockResult('task2')
        task = MockTask(result, 0.003)
        obj.put(task)

        obj.receive()

        obj.end()


    def test_receive_without_put(self):
        obj = CommunicationChannel(tmpdir = self.tmpdir)
        obj.begin()

        self.assertEqual([ ], obj.receive())

        obj.end()

##__________________________________________________________________||
class MockTaskWithProgressReporter(object):
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
class TestCommunicationChannel_ProgressMonitor(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_ProgressMonitor(self):
        progressMonitor = MockProgressMonitor()
        obj = CommunicationChannel(progressMonitor = progressMonitor, tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTaskWithProgressReporter(result1, 0.003)
        obj.put(task1)

        result2 = MockResult('task2')
        task2 = MockTaskWithProgressReporter(result2, 0.001)
        obj.put(task2)

        # the results in the main process don't have a ProgressReporter
        self.assertFalse(hasattr(result1, "progressReporter"))
        self.assertFalse(hasattr(result2, "progressReporter"))

        # the results returned from other processes do.
        returnedResults = obj.receive()
        self.assertIsInstance(returnedResults[0].progressReporter, MockProgressReporter)
        self.assertIsInstance(returnedResults[1].progressReporter, MockProgressReporter)

        obj.end()

##__________________________________________________________________||
class MockTaskWithArguments(object):
    def __init__(self, result, time):
        self.result = result
        self.time = time

    def __call__(self, A, B, C):
        time.sleep(self.time)
        self.result.A = A
        self.result.B = B
        self.result.C = C
        return self.result

##__________________________________________________________________||
class MockTaskWithArgumentsAndProgressReporter(object):
    def __init__(self, result, time):
        self.result = result
        self.time = time

    def __call__(self, A, B, C, progressReporter):
        time.sleep(self.time)
        self.result.A = A
        self.result.B = B
        self.result.C = C
        self.result.progressReporter = progressReporter
        return self.result

##__________________________________________________________________||
class TestCommunicationChannel_task_arguments(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_task_without_ProgressReporterno(self):
        progressMonitor = MockProgressMonitor()
        obj = CommunicationChannel(progressMonitor = progressMonitor, tmpdir = self.tmpdir)
        obj.begin()

        result1 = MockResult('task1')
        task1 = MockTaskWithArguments(result1, 0.003)
        obj.put(task1, 111, 222, 333)

        result2 = MockResult('task2')
        task2 = MockTaskWithArguments(result2, 0.001)
        obj.put(task2, 444, 555, C = 666)

        result3 = MockResult('task3')
        task3 = MockTaskWithArgumentsAndProgressReporter(result3, 0.001)
        obj.put(task3, 777, 888, C = 999)

        # the results in the main process don't have the attributes
        self.assertFalse(hasattr(result1, 'A'))
        self.assertFalse(hasattr(result1, 'B'))
        self.assertFalse(hasattr(result1, 'C'))

        self.assertFalse(hasattr(result2, 'A'))
        self.assertFalse(hasattr(result2, 'B'))
        self.assertFalse(hasattr(result2, 'C'))

        self.assertFalse(hasattr(result3, 'A'))
        self.assertFalse(hasattr(result3, 'B'))
        self.assertFalse(hasattr(result3, 'C'))
        self.assertFalse(hasattr(result3, 'progressReporter'))

        # the results returned from other processes do.
        returnedResults = obj.receive()
        self.assertEqual('task1', returnedResults[0].data)
        self.assertEqual(111, returnedResults[0].A)
        self.assertEqual(222, returnedResults[0].B)
        self.assertEqual(333, returnedResults[0].C)

        self.assertEqual('task2', returnedResults[1].data)
        self.assertEqual(444, returnedResults[1].A)
        self.assertEqual(555, returnedResults[1].B)
        self.assertEqual(666, returnedResults[1].C)

        self.assertEqual('task3', returnedResults[2].data)
        self.assertEqual(777, returnedResults[2].A)
        self.assertEqual(888, returnedResults[2].B)
        self.assertEqual(999, returnedResults[2].C)
        self.assertIsInstance(returnedResults[2].progressReporter, MockProgressReporter)

        obj.end()

##__________________________________________________________________||
