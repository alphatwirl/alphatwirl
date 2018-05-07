# Tai Sakuma <tai.sakuma@gmail.com>
import os
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
from alphatwirl.concurrently import WorkingArea
from alphatwirl.concurrently import SubprocessRunner
from alphatwirl.concurrently import TaskPackageDropbox

from alphatwirl.concurrently.testing import MockResult, MockTask

##__________________________________________________________________||
@pytest.fixture(
    params=[
        'CommunicationChannel0',
        'CommunicationChannel-multiprocessing',
        ## 'CommunicationChannel-subprocess'
    ])
def obj(request, tmpdir_factory, monkeypatch):
    name = request.param
    if name == 'CommunicationChannel0':
        ret = CommunicationChannel0()
    elif name == 'CommunicationChannel-multiprocessing':
        dropbox = MultiprocessingDropbox()
        ret = CommunicationChannel(dropbox=dropbox)
    elif name == 'CommunicationChannel-subprocess':
        topdir = str(tmpdir_factory.mktemp(''))
        topdir = os.path.join(topdir, '_ccsp_temp')
        workingarea = WorkingArea(topdir=topdir, python_modules=( ))
        dropbox = TaskPackageDropbox(
            workingArea=workingarea,
            dispatcher=SubprocessRunner()
        )
        ret = CommunicationChannel(dropbox=dropbox)

    ret.begin()
    yield ret
    ret.end()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_extra_begin(obj):
    obj.begin()

def test_extra_end(obj):
    obj.end()

def test_terminate(obj):
    obj.terminate()

##__________________________________________________________________||
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
def test_put_receive_one_task(obj):
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert [result1] == obj.receive()

def test_receive_without_put(obj):
    assert [ ] == obj.receive()

def test_put_receive_four_tasks(obj):
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)

    assert [result1, result2, result3, result4] == obj.receive()
    # sorted in the order put

def test_put_receive_repeat(obj):
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert [result1, result2] == obj.receive()
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)
    assert [result3, result4] == obj.receive()

def test_put_receive_end_repeat(obj):
    assert 0 == obj.put(task1, *task1_args, **task1_kwargs)
    assert 1 == obj.put(task2, *task2_args, **task2_kwargs)
    assert [result1, result2] == obj.receive()
    obj.end()
    obj.begin()
    assert 2 == obj.put(task3, *task3_args, **task3_kwargs)
    assert 3 == obj.put(task4, *task4_args, **task4_kwargs)
    assert [result3, result4] == obj.receive()

##__________________________________________________________________||
def test_put_multiple_receive_empty(obj):
    assert [ ] == obj.put_multiple([ ])
    assert [ ] == obj.receive()

def test_put_multiple_receive_four_tasks(obj):
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    assert [result1, result2, result3, result4] == obj.receive()
    # sorted in the order put

def test_put_multiple_receive_repeat(obj):
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

def test_put_multiple_receive_end_repeat(obj):
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

##__________________________________________________________________||
def test_put_multiple_receive_all_empty(obj):
    assert [ ] == obj.put_multiple([ ])
    assert [ ] == obj.receive_all()

def test_put_multiple_receive_all_four_tasks(obj):
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    assert [(0, result1), (1, result2), (2, result3), (3, result4)] == obj.receive_all()
    # sorted in the order put

def test_put_multiple_receive_all_repeat(obj):
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

def test_put_multiple_receive_all_end_repeat(obj):
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

##__________________________________________________________________||
def test_receive_finished_four_tasks(obj):
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

##__________________________________________________________________||
def test_receive_finished_then_receive_all(obj):
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

##__________________________________________________________________||
def test_receive_one_four_tasks(obj):
    assert [0, 1, 2, 3] == obj.put_multiple([
        dict(task=task1, args=task1_args, kwargs=task1_kwargs),
        dict(task=task2, args=task2_args, kwargs=task2_kwargs),
        dict(task=task3, args=task3_args, kwargs=task3_kwargs),
        dict(task=task4, args=task4_args, kwargs=task4_kwargs),
    ])

    runid_result_pairs = [ ]
    runid_result_pairs.append(obj.receive_one())
    runid_result_pairs.append(obj.receive_one())
    runid_result_pairs.append(obj.receive_one())
    runid_result_pairs.append(obj.receive_one())

    assert obj.receive_one() is None

    assert sorted([(0, result1), (1, result2), (2, result3), (3, result4)]) == sorted(runid_result_pairs)

##__________________________________________________________________||
