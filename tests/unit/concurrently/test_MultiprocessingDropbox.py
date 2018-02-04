# Tai Sakuma <tai.sakuma@gmail.com>
import time
import os

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

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
@pytest.fixture()
def obj():
    ret = MultiprocessingDropbox()
    ret.open()
    yield ret
    ret.close()

@pytest.fixture()
def package1():
    result1 = MockResult('task1')
    task1 = MockTask(result1, 0.010)
    return TaskPackage(task = task1, args = (), kwargs = {})

@pytest.fixture()
def package2():
    result2 = MockResult('task2')
    task2 = MockTask(result2, 0.001)
    return TaskPackage(task = task2, args = (), kwargs = {})

@pytest.fixture()
def package3():
    result3 = MockResult('task3')
    task3 = MockTask(result3, 0.005)
    return TaskPackage(task = task3, args = (), kwargs = {})

@pytest.fixture()
def package4():
    result4 = MockResult('task4')
    task4 = MockTask(result4, 0.002)
    return TaskPackage(task = task4, args = (), kwargs = {})

##__________________________________________________________________||
def test_repr():
    obj = MultiprocessingDropbox()
    repr(obj)

def test_init_raise():
    with pytest.raises(ValueError):
        MultiprocessingDropbox(nprocesses = 0)

def test_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.close()

def test_open_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.open() # don't create workers again
    obj.close()

def test_put(obj, package1, package2):
    obj.put(package1)
    obj.put(package2)

def test_put_multiple(obj, package1, package2):
    obj.put_multiple([package1, package2])

def test_put_receive(obj, package1, package2):
    obj.put(package1)
    obj.put(package2)
    actual = [r.data for r in obj.receive()]
    assert set(['task1', 'task2']) == set(actual)

def test_receive_order(obj, package1, package2, package3):
    # results of tasks are sorted in the order in which the tasks are
    # put.
    obj.put(package1)
    obj.put(package2)
    obj.put(package3)
    actual = [r.data for r in obj.receive()]
    assert ['task1', 'task2', 'task3'] == actual

def test_put_receive_repeat(obj, package1, package2, package3, package4):

    obj.put(package1)
    obj.put(package2)
    actual = [r.data for r in obj.receive()]
    assert set(['task1', 'task2']) == set(actual)

    obj.put(package3)
    obj.put(package4)
    actual = [r.data for r in obj.receive()]
    assert set(['task3', 'task4']) == set(actual)

def test_begin_put_recive_end_repeat(obj, package1, package2):

    obj.put(package1)
    obj.receive()
    obj.close()
    obj.open()
    obj.put(package2)
    obj.receive()

def test_terminate(obj, package1, package2):

    obj.put(package1)
    obj.put(package2)
    obj.terminate()

def test_receive_without_put(obj):
    assert [ ] == obj.receive()

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
    def createReporter(obj): return MockProgressReporter()
    def monitor(obj): pass
    def last(obj): pass

##__________________________________________________________________||
def test_ProgressMonitor():
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
    assert not hasattr(result1, "progressReporter")
    assert not hasattr(result2, "progressReporter")

    # the results returned from other processes do.
    returnedResults = obj.receive()
    assert isinstance(returnedResults[0].progressReporter, MockProgressReporter)
    assert isinstance(returnedResults[1].progressReporter, MockProgressReporter)

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
def test_task_without_ProgressReporterno():
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
    assert not hasattr(result1, 'A')
    assert not hasattr(result1, 'B')
    assert not hasattr(result1, 'C')

    assert not hasattr(result2, 'A')
    assert not hasattr(result2, 'B')
    assert not hasattr(result2, 'C')

    assert not hasattr(result3, 'A')
    assert not hasattr(result3, 'B')
    assert not hasattr(result3, 'C')
    assert not hasattr(result3, 'progressReporter')

    # the results returned from other processes do.
    returnedResults = obj.receive()
    assert 'task1' == returnedResults[0].data
    assert 111 == returnedResults[0].A
    assert 222 == returnedResults[0].B
    assert 333 == returnedResults[0].C

    assert 'task2' == returnedResults[1].data
    assert 444 == returnedResults[1].A
    assert 555 == returnedResults[1].B
    assert 666 == returnedResults[1].C

    assert 'task3' == returnedResults[2].data
    assert 777 == returnedResults[2].A
    assert 888 == returnedResults[2].B
    assert 999 == returnedResults[2].C
    assert isinstance(returnedResults[2].progressReporter, MockProgressReporter)

    obj.close()

##__________________________________________________________________||
