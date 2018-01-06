# Tai Sakuma <tai.sakuma@gmail.com>
import collections
import logging

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel, TaskPackage

##__________________________________________________________________||
MockTask = collections.namedtuple('MockTask', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class MockProgressReporter(object): pass

##__________________________________________________________________||
class MockProgressMonitor(object):
    def __init__(self):
        self.reporters = [ ]

    def createReporter(self):
        reporter = MockProgressReporter()
        self.reporters.append(reporter)
        return reporter

##__________________________________________________________________||
class MockDropbox(object):
    pass

@pytest.fixture()
def dropbox():
    ret = MockDropbox()
    ret.open = mock.MagicMock()
    ret.close = mock.MagicMock()
    ret.put = mock.MagicMock()
    return ret

@pytest.fixture()
def obj(dropbox):
    return CommunicationChannel(dropbox = dropbox)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin_end(obj, dropbox):

    dropbox.open.assert_not_called()
    dropbox.close.assert_not_called()

    obj.begin()
    dropbox.open.assert_called_once()
    dropbox.close.assert_not_called()

    obj.begin()
    dropbox.open.assert_called_once() # don't open twice
    dropbox.close.assert_not_called()

    obj.end()
    dropbox.open.assert_called_once()
    dropbox.close.assert_called_once()

    obj.end()
    dropbox.open.assert_called_once()
    dropbox.close.assert_called_once() # don't close twice

    obj.begin()
    assert 2 == dropbox.open.call_count # can open again
    dropbox.close.assert_called_once()

def test_put(obj, dropbox):

    obj.begin()

    task1 = MockTask('task1')
    obj.put(task1)

    task2 = MockTask('task2')
    obj.put(task2, 123, 'ABC', A = 34)

    expected = [
        mock.call(TaskPackage(task = task1, args = (), kwargs = {})),
        mock.call(TaskPackage(task = task2, args = (123, 'ABC'), kwargs = {'A': 34})),
    ]
    dropbox.put.assert_has_calls(expected)

    obj.end()

def test_receive(obj, dropbox):

    obj.begin()

    result1 = MockResult('result1')
    dropbox.receive = mock.MagicMock(return_value = result1)

    assert result1 == obj.receive()

    obj.end()

def test_put_when_closed(obj, dropbox):

    # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
    task1 = MockTask('task1')
    obj.put(task1)

    dropbox.put.assert_not_called()

def test_receive_when_closed(obj, dropbox):

    # logging.getLogger('alphatwirl').setLevel(logging.DEBUG)
    result1 = MockResult('result1')
    dropbox.receive = mock.MagicMock(return_value = result1)
    assert obj.receive() is None

    obj.end()

##__________________________________________________________________||
