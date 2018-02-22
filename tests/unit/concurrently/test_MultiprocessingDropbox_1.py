# Tai Sakuma <tai.sakuma@gmail.com>
import os
import time
import collections

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import MultiprocessingDropbox
from alphatwirl.concurrently import TaskPackage

##__________________________________________________________________||
def test_init_raise():
    with pytest.raises(ValueError):
        MultiprocessingDropbox(nprocesses=0)

def test_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.close()

def test_open_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.open() # don't create workers again
    obj.close()

def test_repr():
    obj = MultiprocessingDropbox()
    repr(obj)

##__________________________________________________________________||
class MockTask(object):
    def __init__(self, result, time):
        self.result = result
        self.time = time

    def __call__(self):
        time.sleep(self.time)
        return self.result

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'data')

##__________________________________________________________________||
@pytest.fixture()
def package1():
    result1 = MockResult('result1')
    task1 = MockTask(result1, 0.010)
    return TaskPackage(task=task1, args=(), kwargs={})

@pytest.fixture()
def package2():
    result2 = MockResult('result2')
    task2 = MockTask(result2, 0.001)
    return TaskPackage(task=task2, args=(), kwargs={})

@pytest.fixture()
def package3():
    result3 = MockResult('result3')
    task3 = MockTask(result3, 0.005)
    return TaskPackage(task=task3, args=(), kwargs={})

@pytest.fixture()
def package4():
    result4 = MockResult('result4')
    task4 = MockTask(result4, 0.002)
    return TaskPackage(task=task4, args=(), kwargs={})

@pytest.fixture()
def obj():
    ret = MultiprocessingDropbox()
    ret.open()
    yield ret
    ret.close()

##__________________________________________________________________||
def test_put(obj, package1, package2):
    obj.put(package1)
    obj.put(package2)

def test_put_multiple(obj, package1, package2):
    obj.put_multiple([package1, package2])

def test_put_receive(obj, package1, package2):
    obj.put(package1)
    obj.put(package2)
    expected = [MockResult('result1'), MockResult('result2')]
    actual = obj.receive()
    assert expected == actual

def test_receive_order(obj, package1, package2, package3):
    # results of tasks are sorted in the order in which the tasks are put.
    obj.put(package1)
    obj.put(package2)
    obj.put(package3)
    expected = [MockResult('result1'), MockResult('result2'), MockResult('result3')]
    actual = obj.receive()
    assert expected == actual

def test_put_receive_repeat(obj, package1, package2, package3, package4):

    obj.put(package1)
    obj.put(package2)
    expected = [MockResult('result1'), MockResult('result2')]
    actual = obj.receive()
    assert expected == actual

    obj.put(package3)
    obj.put(package4)
    expected = [MockResult('result3'), MockResult('result4')]
    actual = obj.receive()
    assert expected == actual

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
