# Tai Sakuma <tai.sakuma@cern.ch>
import unittest
import time
import os

from alphatwirl.concurrently import MultiprocessingDropbox
from alphatwirl.concurrently import TaskPackage

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
class TestMultiprocessingDropbox(unittest.TestCase):

    def test_repr(self):
        obj = MultiprocessingDropbox()
        repr(obj)

    def test_init_raise(self):
        self.assertRaises(ValueError, MultiprocessingDropbox, nprocesses = 0)

    def test_open_close(self):
        obj = MultiprocessingDropbox()
        obj.open()
        obj.close()

    def test_open_open_close(self):
        obj = MultiprocessingDropbox()
        obj.open()
        obj.open() # don't create workers again
        obj.close()

    def test_put(self):
        obj = MultiprocessingDropbox()
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        package1 = TaskPackage(task = task1, args = (), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (), kwargs = {})
        obj.put(package2)

        obj.close()

    def test_put_receive(self):
        obj = MultiprocessingDropbox()
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        package1 = TaskPackage(task = task1, args = (), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (), kwargs = {})
        obj.put(package2)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task1', 'task2']), set(actual))

        obj.close()

    def test_receive_order(self):
        # results of tasks are sorted in the order in which the tasks
        # are put.

        obj = MultiprocessingDropbox()
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.010)
        package1 = TaskPackage(task = task1, args = (), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (), kwargs = {})
        obj.put(package2)

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.005)
        package3 = TaskPackage(task = task3, args = (), kwargs = {})
        obj.put(package3)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(['task1', 'task2', 'task3'], actual)

        obj.close()

    def test_put_receive_repeat(self):
        obj = MultiprocessingDropbox()
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTask(result1, 0.003)
        package1 = TaskPackage(task = task1, args = (), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTask(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (), kwargs = {})
        obj.put(package2)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task1', 'task2']), set(actual))

        result3 = MockResult('task3')
        task3 = MockTask(result3, 0.002)
        package3 = TaskPackage(task = task3, args = (), kwargs = {})
        obj.put(package3)

        result4 = MockResult('task4')
        task4 = MockTask(result4, 0.002)
        package4 = TaskPackage(task = task4, args = (), kwargs = {})
        obj.put(package4)

        actual = [r.data for r in obj.receive()]
        self.assertEqual(set(['task3', 'task4']), set(actual))

        obj.close()

    def test_begin_put_recive_end_repeat(self):
        obj = MultiprocessingDropbox()
        obj.open()

        result = MockResult('task1')
        task = MockTask(result, 0.003)
        package = TaskPackage(task = task, args = (), kwargs = {})
        obj.put(package)

        obj.receive()

        obj.close()

        obj.open()

        result = MockResult('task2')
        task = MockTask(result, 0.003)
        package = TaskPackage(task = task, args = (), kwargs = {})
        obj.put(package)

        obj.receive()

        obj.close()


    def test_receive_without_put(self):
        obj = MultiprocessingDropbox()
        obj.open()

        self.assertEqual([ ], obj.receive())

        obj.close()

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
class TestMultiprocessingDropbox_ProgressMonitor(unittest.TestCase):

    def test_ProgressMonitor(self):
        progressMonitor = MockProgressMonitor()
        obj = MultiprocessingDropbox(nprocesses = 3, progressMonitor = progressMonitor)
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTaskWithProgressReporter(result1, 0.003)
        package1 = TaskPackage(task = task1, args = (), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTaskWithProgressReporter(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (), kwargs = {})
        obj.put(package2)

        # the results in the main process don't have a ProgressReporter
        self.assertFalse(hasattr(result1, "progressReporter"))
        self.assertFalse(hasattr(result2, "progressReporter"))

        # the results returned from other processes do.
        returnedResults = obj.receive()
        self.assertIsInstance(returnedResults[0].progressReporter, MockProgressReporter)
        self.assertIsInstance(returnedResults[1].progressReporter, MockProgressReporter)

        obj.close()

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
class TestMultiprocessingDropbox_task_arguments(unittest.TestCase):

    def test_task_without_ProgressReporterno(self):
        progressMonitor = MockProgressMonitor()
        obj = MultiprocessingDropbox(nprocesses = 3, progressMonitor = progressMonitor)
        obj.open()

        result1 = MockResult('task1')
        task1 = MockTaskWithArguments(result1, 0.003)
        package1 = TaskPackage(task = task1, args = (111, 222, 333), kwargs = {})
        obj.put(package1)

        result2 = MockResult('task2')
        task2 = MockTaskWithArguments(result2, 0.001)
        package2 = TaskPackage(task = task2, args = (444, 555), kwargs = dict(C = 666))
        obj.put(package2)

        result3 = MockResult('task3')
        task3 = MockTaskWithArgumentsAndProgressReporter(result3, 0.001)
        package3 = TaskPackage(task = task3, args = (777, 888), kwargs = dict(C = 999))
        obj.put(package3)

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

        obj.close()

##__________________________________________________________________||
