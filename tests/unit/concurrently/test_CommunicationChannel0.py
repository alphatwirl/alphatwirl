# Tai Sakuma <tai.sakuma@gmail.com>

import pytest
import time

from alphatwirl.concurrently import CommunicationChannel0

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
@pytest.fixture()
def obj():
    return CommunicationChannel0()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_begin_end(obj):
    obj.begin()
    obj.end()

##__________________________________________________________________||
def test_begin_begin_end(obj):
    obj.begin()
    obj.begin()
    obj.end()

##__________________________________________________________________||
def test_put(obj):
    obj.begin()

    result1 = MockResult('task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = MockResult('task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    obj.end()

##__________________________________________________________________||
def test_put_receive(obj):
    obj.begin()

    result1 = MockResult('task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = MockResult('task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    actual = [r.data for r in obj.receive()]
    assert set(['task1', 'task2']) == set(actual)

    obj.end()

##__________________________________________________________________||
def test_receive_order(obj):
    # results of tasks are sorted in the order in which the tasks are
    # put.

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
    assert ['task1', 'task2', 'task3'] == actual

    obj.end()

##__________________________________________________________________||
def test_put_receive_repeat(obj):
    obj.begin()

    result1 = MockResult('task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = MockResult('task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    actual = [r.data for r in obj.receive()]
    assert set(['task1', 'task2']) == set(actual)

    result3 = MockResult('task3')
    task3 = MockTask(result3, 0.002)
    obj.put(task3)

    result4 = MockResult('task4')
    task4 = MockTask(result4, 0.002)
    obj.put(task4)

    actual = [r.data for r in obj.receive()]
    assert set(['task3', 'task4']) == set(actual)

    obj.end()

##__________________________________________________________________||
def test_begin_put_recive_end_repeat(obj):

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

##__________________________________________________________________||
def test_receive_without_put(obj):
    obj.begin()

    assert [ ] == obj.receive()

    obj.end()

##__________________________________________________________________||
