# Tai Sakuma <tai.sakuma@gmail.com>
import time
import functools

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import MultiprocessingDropbox

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
def task(sleep, ret):
    time.sleep(sleep)
    return ret

@pytest.fixture()
def obj():
    ret = MultiprocessingDropbox()
    ret.open()
    yield ret
    ret.terminate()
    ret.close()

@pytest.fixture()
def expected(obj):
    idx1 = obj.put(functools.partial(task, 0.010, 'result1'))
    idx2 = obj.put(functools.partial(task, 0.001, 'result2'))
    idx3, idx4 = obj.put_multiple([
        functools.partial(task, 0.010, 'result3'),
        functools.partial(task, 0.001, 'result4'),
    ])

    ret = [
        (idx1, 'result1'),
        (idx2, 'result2'),
        (idx3, 'result3'),
        (idx4, 'result4'),
    ]
    yield ret

##__________________________________________________________________||
def test_receive(obj, expected):
    actual = obj.receive()
    assert expected == actual

def test_poll(obj, expected):
    actual = [ ]
    while len(actual) < len(expected):
        actual.extend(obj.poll())
    assert sorted(expected) == sorted(actual)

def test_receive_one(obj, expected):
    actual = [ ]
    for i in range(len(expected)):
        actual.append(obj.receive_one())
    assert obj.receive_one() is None
    assert sorted(expected) == sorted(actual)

##__________________________________________________________________||
