# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import EventLoopRunner

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return EventLoopRunner()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj):
    obj.begin()

def test_end(obj):
    obj.begin()
    assert [ ] == obj.end()

def test_run(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1
    assert 0 == obj.run(eventLoop1)

    assert [mock.call()] == eventLoop1.call_args_list

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2
    assert 1 == obj.run(eventLoop2)

    assert [mock.call()] == eventLoop2.call_args_list

    assert [result1, result2] == obj.end()

def test_run_multiple(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2

    assert [0, 1] == obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call()] == eventLoop1.call_args_list
    assert [mock.call()] == eventLoop2.call_args_list

    assert [result1, result2] == obj.end()
    assert [ ] == obj.end()

##__________________________________________________________________||
def test_receive(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2

    assert [0, 1] == obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call()] == eventLoop1.call_args_list
    assert [mock.call()] == eventLoop2.call_args_list

    assert [(0, result1), (1, result2)] == obj.receive()
    assert [ ] == obj.receive()

def test_poll(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2

    assert [0, 1] == obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call()] == eventLoop1.call_args_list
    assert [mock.call()] == eventLoop2.call_args_list

    assert [(0, result1), (1, result2)] == obj.poll()
    assert [ ] == obj.poll()

def test_receive_one(obj):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2

    assert [0, 1] == obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call()] == eventLoop1.call_args_list
    assert [mock.call()] == eventLoop2.call_args_list

    assert (0, result1) == obj.receive_one()
    assert (1, result2) == obj.receive_one()
    assert obj.receive_one() is None

##__________________________________________________________________||

