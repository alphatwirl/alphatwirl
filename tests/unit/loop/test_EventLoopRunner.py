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
def progressReporter():
    return mock.Mock(name='progressReporter')

@pytest.fixture()
def progressMonitor(progressReporter):
    ret = mock.Mock(name='progressMonitor')
    ret.createReporter.return_value = progressReporter
    return ret

@pytest.fixture()
def obj(progressMonitor):
    return EventLoopRunner(progressMonitor=progressMonitor)

##__________________________________________________________________||
def test_repr(obj):
   repr(obj)

def test_begin(obj):
    obj.begin()

def test_end(obj):
    obj.begin()
    assert [ ] == obj.end()

def test_run(obj, progressReporter):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1
    obj.run(eventLoop1)

    assert [mock.call(progressReporter=progressReporter)] == eventLoop1.call_args_list

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2
    obj.run(eventLoop2)

    assert [mock.call(progressReporter=progressReporter)] == eventLoop2.call_args_list

    assert [result1, result2] == obj.end()

def test_run_multiple(obj, progressReporter):
    obj.begin()

    result1 = mock.Mock(name='result1')
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop1.return_value = result1

    result2 = mock.Mock(name='result2')
    eventLoop2 = mock.Mock(name='eventLoop2')
    eventLoop2.return_value = result2

    obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call(progressReporter=progressReporter)] == eventLoop1.call_args_list
    assert [mock.call(progressReporter=progressReporter)] == eventLoop2.call_args_list

    assert [result1, result2] == obj.end()

##__________________________________________________________________||

