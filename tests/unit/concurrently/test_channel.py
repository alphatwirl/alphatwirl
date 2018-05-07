# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import time
import collections

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel
from alphatwirl.concurrently import CommunicationChannel0
from alphatwirl.concurrently import MultiprocessingDropbox

##__________________________________________________________________||
def channel_multiprocessing():
    dropbox = MultiprocessingDropbox()
    ret = CommunicationChannel(dropbox=dropbox)
    return ret

obj_factories = [CommunicationChannel0, channel_multiprocessing]
obj_names = ['CommunicationChannel0', 'CommunicationChannel-multiprocessing']

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_repr(factory):
    obj = factory()
    repr(obj)

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_begin_end(factory):
    obj = factory()
    obj.begin()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_begin_begin_end(factory):
    obj = factory()
    obj.begin()
    obj.begin()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_begin_begin_terminate_end(factory):
    obj = factory()
    obj.begin()
    obj.terminate()
    obj.end()

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'name args kwargs')

class MockTask(object):
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __call__(self, *args, **kwargs):
        time.sleep(self.time)
        return MockResult(name=self.name, args=args, kwargs=kwargs)

task1 = MockTask(name='task1', time=0.01)
task1_args = (123, 'ABC')
task1_kwargs = {'A': 34}
result1 = MockResult(name='task1', args=task1_args, kwargs=task1_kwargs)

task2 = MockTask(name='task2', time=0.001)
task2_args = ( )
task2_kwargs = { }
result2 = MockResult(name='task2', args=task2_args, kwargs=task2_kwargs)

task3 = MockTask(name='task3', time=0.005)
task3_args = (33, 44)
task3_kwargs = { }
result3 = MockResult(name='task3', args=task3_args, kwargs=task3_kwargs)

task4 = MockTask(name='task4', time=0.002)
task4_args = ( )
task4_kwargs = dict(ABC='abc', DEF='def')
result4 = MockResult(name='task4', args=task4_args, kwargs=task4_kwargs)

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_receive_one_task(factory):
    obj = factory()
    obj.begin()
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert [result1] == obj.receive()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_receive_without_put(factory):
    obj = factory()
    obj.begin()
    assert [ ] == obj.receive()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_receive_four_tasks(factory):
    obj = factory()
    obj.begin()
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)

    assert [result1, result2, result3, result4] == obj.receive()
    # sorted in the order put

    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_receive_repeat(factory):
    obj = factory()
    obj.begin()
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert [result1, result2] == obj.receive()
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)
    assert [result3, result4] == obj.receive()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_receive_end_repeat(factory):
    obj = factory()
    obj.begin()
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert [result1, result2] == obj.receive()
    obj.end()
    obj.begin()
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)
    assert [result3, result4] == obj.receive()
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_empty(factory):
    obj = factory()
    obj.begin()
    assert [ ] == obj.put_multiple([ ])
    assert [ ] == obj.receive()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_four_tasks(factory):
    obj = factory()
    obj.begin()
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    assert [result1, result2, result3, result4] == obj.receive()
    # sorted in the order put

    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_repeat(factory):
    obj = factory()
    obj.begin()
    assert [0, 1] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
    ])
    assert [result1, result2] == obj.receive()
    assert [2, 3] == obj.put_multiple([
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])
    assert [result3, result4] == obj.receive()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_end_repeat(factory):
    obj = factory()
    obj.begin()
    assert [0, 1] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
    ])
    assert [result1, result2] == obj.receive()
    obj.end()
    obj.begin()
    assert [2, 3] == obj.put_multiple([
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])
    assert [result3, result4] == obj.receive()
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_all_empty(factory):
    obj = factory()
    obj.begin()
    assert [ ] == obj.put_multiple([ ])
    assert [ ] == obj.receive_all()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_all_four_tasks(factory):
    obj = factory()
    obj.begin()
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    assert [(0, result1), (1, result2), (2, result3), (3, result4)] == obj.receive_all()
    # sorted in the order put

    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_all_repeat(factory):
    obj = factory()
    obj.begin()
    assert [0, 1] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
    ])
    assert [(0, result1), (1, result2)] == obj.receive_all()
    assert [2, 3] == obj.put_multiple([
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])
    assert [(2, result3), (3, result4)] == obj.receive_all()
    obj.end()

@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_put_multiple_receive_all_end_repeat(factory):
    obj = factory()
    obj.begin()
    assert [0, 1] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
    ])
    assert [(0, result1), (1, result2)] == obj.receive_all()
    obj.end()
    obj.begin()
    assert [2, 3] == obj.put_multiple([
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])
    assert [(2, result3), (3, result4)] == obj.receive_all()
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_receive_finished_four_tasks(factory):
    obj = factory()
    obj.begin()
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    runid_result_pairs = [ ]
    ntasks_to_wait = 4
    while len(runid_result_pairs) < ntasks_to_wait:
        runid_result_pairs.extend(obj.receive_finished())

    assert sorted([(0, result1), (1, result2), (2, result3), (3, result4)]) == sorted(runid_result_pairs)

    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('factory', obj_factories, ids=obj_names)
def test_receive_finished_then_receive_all(factory):
    obj = factory()
    obj.begin()
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    runid_result_pairs = [ ]

    # receive the first two with receive_finished()
    ntasks_to_wait = 2
    while len(runid_result_pairs) < ntasks_to_wait:
        runid_result_pairs.extend(obj.receive_finished())

    # the rest with receive_all()
    runid_result_pairs.extend(obj.receive_all())

    assert sorted([(0, result1), (1, result2), (2, result3), (3, result4)]) == sorted(runid_result_pairs)

    obj.end()

##__________________________________________________________________||
