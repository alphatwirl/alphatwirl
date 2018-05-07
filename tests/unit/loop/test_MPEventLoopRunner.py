# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import MPEventLoopRunner

##__________________________________________________________________||
@pytest.fixture()
def communicationChannel():
    return mock.Mock(name='communicationChannel')

@pytest.fixture()
def obj(communicationChannel):
    return MPEventLoopRunner(communicationChannel)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin_end(obj, communicationChannel):
    obj.begin()
    communicationChannel.receive.return_value = [ ]
    obj.end()

def test_run(obj, communicationChannel):
    obj.begin()

    communicationChannel.put.side_effect = [0, 1]

    eventLoop1 = mock.Mock(name='eventLoop1')
    assert 0 == obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    assert 1 == obj.run(eventLoop2)

    assert [mock.call(eventLoop1), mock.call(eventLoop2)] == communicationChannel.put.call_args_list

def test_run_multiple(obj, communicationChannel):
    obj.begin()
    communicationChannel.put_multiple.return_value = [0, 1]
    eventLoop1 = mock.Mock(name='eventLoop1')
    eventLoop2 = mock.Mock(name='eventLoop2')
    assert [0, 1] == obj.run_multiple([eventLoop1, eventLoop2])

    assert [mock.call([eventLoop1, eventLoop2])] == communicationChannel.put_multiple.call_args_list

def test_end(obj, communicationChannel):
    obj.begin()

    eventLoop1 = mock.Mock(name='eventLoop1')
    obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    obj.run(eventLoop2)

    result1 = mock.Mock(name='result1')
    result2 = mock.Mock(name='result2')
    communicationChannel.receive.return_value = [result1, result2]
    assert [result1, result2] == obj.end()

def test_end_logging_wrong_number_or_results(obj, communicationChannel, caplog):
    obj.begin()

    eventLoop1 = mock.Mock(name='eventLoop1')
    obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    obj.run(eventLoop2)

    result1 = mock.Mock(name='result1')
    result2 = mock.Mock(name='result2')
    communicationChannel.receive.return_value = [result1]

    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        results = obj.end()

    assert [result1] == results

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'MPEventLoopRunner' in caplog.records[0].name
    assert 'too few results received' in caplog.records[0].msg

##__________________________________________________________________||
def test_receive(obj, communicationChannel):
    obj.begin()

    communicationChannel.put.side_effect = [0, 1]

    eventLoop1 = mock.Mock(name='eventLoop1')
    assert 0 == obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    assert 1 == obj.run(eventLoop2)

    result1 = mock.Mock(name='result1')
    result2 = mock.Mock(name='result2')
    communicationChannel.receive_all.return_value = [(0, result1), (1, result2)]
    assert [(0, result1), (1, result2)] == obj.receive()

def test_poll(obj, communicationChannel):
    obj.begin()

    communicationChannel.put.side_effect = [0, 1]

    eventLoop1 = mock.Mock(name='eventLoop1')
    assert 0 == obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    assert 1 == obj.run(eventLoop2)

    result1 = mock.Mock(name='result1')
    result2 = mock.Mock(name='result2')
    communicationChannel.receive_finished.return_value = [(0, result1), (1, result2)]
    assert [(0, result1), (1, result2)] == obj.poll()

def test_receive_one(obj, communicationChannel):
    obj.begin()

    communicationChannel.put.side_effect = [0, 1]

    eventLoop1 = mock.Mock(name='eventLoop1')
    assert 0 == obj.run(eventLoop1)

    eventLoop2 = mock.Mock(name='eventLoop2')
    assert 1 == obj.run(eventLoop2)

    result1 = mock.Mock(name='result1')
    result2 = mock.Mock(name='result2')

    communicationChannel.receive_one.side_effect = [(0, result1), (1, result2), None]
    assert (0, result1) == obj.receive_one()
    assert (1, result2) == obj.receive_one()
    assert obj.receive_one() is None

##__________________________________________________________________||
