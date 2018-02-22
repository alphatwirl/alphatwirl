# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel0

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
def test_put_receive(obj):
    obj.begin()
    result1 = mock.Mock(name='result1')
    task1 = mock.Mock(name='task1')
    task1.return_value = result1
    obj.put(task1, 123, 'ABC', A=34)
    assert [mock.call(123, 'ABC', A=34)] == task1.call_args_list
    assert [result1] == obj.receive()
    obj.end()

##__________________________________________________________________||
def test_receive_order(obj):
    # results of tasks are sorted in the order in which the tasks are
    # put.

    obj.begin()

    result1 = mock.Mock(name='result1')
    task1 = mock.Mock(name='task1')
    task1.return_value = result1
    obj.put(task1)

    result2 = mock.Mock(name='result2')
    task2 = mock.Mock(name='task2')
    task2.return_value = result2
    obj.put(task2)

    result3 = mock.Mock(name='result3')
    task3 = mock.Mock(name='task3')
    task3.return_value = result3
    obj.put(task3)

    assert [result1, result2, result3] == obj.receive()

    obj.end()

##__________________________________________________________________||
def test_put_receive_repeat(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    task1 = mock.Mock(name='task1')
    task1.return_value = result1
    obj.put(task1)

    result2 = mock.Mock(name='result2')
    task2 = mock.Mock(name='task2')
    task2.return_value = result2
    obj.put(task2)

    assert [result1, result2] == obj.receive()

    result3 = mock.Mock(name='result3')
    task3 = mock.Mock(name='task3')
    task3.return_value = result3
    obj.put(task3)

    result4 = mock.Mock(name='result4')
    task4 = mock.Mock(name='task4')
    task4.return_value = result4
    obj.put(task4)

    assert [result3, result4] == obj.receive()

    obj.end()

##__________________________________________________________________||
def test_begin_put_recive_end_repeat(obj):

    obj.begin()

    result1 = mock.Mock(name='result1')
    task1 = mock.Mock(name='task1')
    task1.return_value = result1
    obj.put(task1)

    obj.receive()

    obj.end()

    obj.begin()

    result2 = mock.Mock(name='result2')
    task2 = mock.Mock(name='task2')
    task2.return_value = result2
    obj.put(task2)

    obj.receive()

    obj.end()

##__________________________________________________________________||
def test_receive_without_put(obj):
    obj.begin()

    assert [ ] == obj.receive()

    obj.end()

##__________________________________________________________________||
def test_put_multiple(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    task1 = mock.Mock(name='task1')
    task1.return_value = result1

    result2 = mock.Mock(name='result2')
    task2 = mock.Mock(name='task2')
    task2.return_value = result2

    result3 = mock.Mock(name='result3')
    task3 = mock.Mock(name='task3')
    task3.return_value = result3

    result4 = mock.Mock(name='result4')
    task4 = mock.Mock(name='task4')
    task4.return_value = result4

    obj.put_multiple([
        task1,
        dict(task=task2, args=(123, 'ABC'), kwargs={'A': 34}),
        dict(task=task3, kwargs={'B': 123}),
        dict(task=task4, args=(222, 'def')),
    ])

    assert [mock.call()] == task1.call_args_list
    assert [mock.call(123, 'ABC', A=34)] == task2.call_args_list
    assert [mock.call(B=123)] == task3.call_args_list
    assert [mock.call(222, 'def')] == task4.call_args_list
    assert [result1, result2, result3, result4] == obj.receive()

    obj.end()

##__________________________________________________________________||
