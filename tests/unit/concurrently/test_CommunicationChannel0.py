# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import time

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel0

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
def test_begin_begin_terminate_end(obj):
    obj.begin()
    obj.terminate()
    obj.end()

##__________________________________________________________________||
def test_put(obj):
    obj.begin()

    result1 = mock.MagicMock(name='task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = mock.MagicMock(name='task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    obj.end()

##__________________________________________________________________||
def test_put_receive(obj):
    obj.begin()

    result1 = mock.MagicMock(name='task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = mock.MagicMock(name='task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    assert set([result1, result2]) == set(obj.receive())

    obj.end()

##__________________________________________________________________||
def test_receive_order(obj):
    # results of tasks are sorted in the order in which the tasks are
    # put.

    obj.begin()

    result1 = mock.MagicMock(name='task1')
    task1 = MockTask(result1, 0.010)
    obj.put(task1)

    result2 = mock.MagicMock(name='task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    result3 = mock.MagicMock(name='task3')
    task3 = MockTask(result3, 0.005)
    obj.put(task3)

    assert [result1, result2, result3] == obj.receive()

    obj.end()

##__________________________________________________________________||
def test_put_receive_repeat(obj):
    obj.begin()

    result1 = mock.MagicMock(name='task1')
    task1 = MockTask(result1, 0.003)
    obj.put(task1)

    result2 = mock.MagicMock(name='task2')
    task2 = MockTask(result2, 0.001)
    obj.put(task2)

    assert set([result1, result2]) == set(obj.receive())

    result3 = mock.MagicMock(name='task3')
    task3 = MockTask(result3, 0.002)
    obj.put(task3)

    result4 = mock.MagicMock(name='task4')
    task4 = MockTask(result4, 0.002)
    obj.put(task4)

    assert set([result3, result4]) == set(obj.receive())

    obj.end()

##__________________________________________________________________||
def test_begin_put_recive_end_repeat(obj):

    obj.begin()

    result = mock.MagicMock(name='task1')
    task = MockTask(result, 0.003)
    obj.put(task)

    obj.receive()

    obj.end()

    obj.begin()

    result = mock.MagicMock(name='task2')
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
