# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest
from collections import deque

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import TaskPackageDropbox

##__________________________________________________________________||
@pytest.fixture()
def packages():
    return [
        mock.Mock(name='package0'),
        mock.Mock(name='package1'),
        mock.Mock(name='package2'),
        mock.Mock(name='package3'),
        mock.Mock(name='package4'),
    ]

@pytest.fixture()
def pkgidx_result_pairs(results):
    # e.g., [(0, package0), (1, package1), ...]
    return list(enumerate(results))

@pytest.fixture()
def results():
    return [
        mock.Mock(name='result0'),
        mock.Mock(name='result1'),
        mock.Mock(name='result2'),
        mock.Mock(name='result3'),
        mock.Mock(name='result4'),
    ]

@pytest.fixture()
def collect_results(results):
    ret = {i: deque([r]) for i, r in enumerate(results)}
    # e.g., {0: deque([result0]), 1:deque([result1]), ...}

    # 3rd job fails twice before succeed
    ret[2].extendleft([None, None])
    # e.g., deque([None, None, result2])

    return ret

@pytest.fixture()
def workingarea(collect_results):
    ret = mock.MagicMock()
    ret.put_package.side_effect = [0, 1, 2, 3, 4] # package indices
    ret.collect_result.side_effect = lambda i: collect_results[i].popleft()
    return ret

@pytest.fixture()
def dispatcher():
    ret = mock.MagicMock()
    ret.run_multiple.return_value = [1000, 1001, 1002, 1003, 1004]

    # jobs finish in steps
    ret.poll.side_effect = [
        [1001, 1003],
        [ ],
        [1002],
        [1000, 1005],
        [1006, 1004]
    ]

    # for resubmission
    ret.run.side_effect = [1005, 1006]

    return ret

@pytest.fixture()
def obj(workingarea, dispatcher, packages):
    ret = TaskPackageDropbox(workingArea=workingarea, dispatcher=dispatcher, sleep=0.01)
    ret.open()
    ret.put_multiple(packages)
    yield ret
    ret.close()

##__________________________________________________________________||
def test_receive(obj, pkgidx_result_pairs):
    assert pkgidx_result_pairs == obj.receive()

def test_receive_dispatcher_received_failed_runids(obj, dispatcher):
    obj.receive()
    assert [
        mock.call([]), mock.call([]), mock.call([1002]),
        mock.call([1005]), mock.call([])
    ] == dispatcher.failed_runids.call_args_list

def test_receive_logging_resubmission(obj, caplog):
    with caplog.at_level(logging.WARNING):
        obj.receive()
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[1].levelname == 'WARNING'
    assert 'TaskPackageDropbox' in caplog.records[0].name
    assert 'TaskPackageDropbox' in caplog.records[1].name
    assert 'resubmitting' in caplog.records[0].msg
    assert 'resubmitting' in caplog.records[1].msg

def test_receive_in_one_step(obj, pkgidx_result_pairs, dispatcher, collect_results):

    # make all jobs finish by the first poll
    dispatcher.poll.side_effect = [[1000, 1001, 1002, 1003, 1004]]

    # make the 3rd job successful by removing two None's
    collect_results[2].popleft() # deque([None, result2])
    collect_results[2].popleft() # deque([result2])

    assert pkgidx_result_pairs == obj.receive()

##__________________________________________________________________||
def test_poll(obj, pkgidx_result_pairs):
    actual = [ ]
    while len(actual) < len(pkgidx_result_pairs):
        actual.extend(obj.poll())
    assert sorted(pkgidx_result_pairs) == sorted(actual)

def test_poll_then_receive(obj, pkgidx_result_pairs):
    actual = [ ]
    actual.extend(obj.poll())
    actual.extend(obj.receive())

    assert sorted(pkgidx_result_pairs) == sorted(actual)

##__________________________________________________________________||
def test_receive_one(obj, pkgidx_result_pairs):
    actual = [ ]
    while len(actual) < len(pkgidx_result_pairs):
        pair = obj.receive_one()
        if pair is None:
            break
        actual.append(pair)
    assert obj.receive_one() is None
    assert sorted(pkgidx_result_pairs) == sorted(actual)

@pytest.mark.parametrize('dispatcher_poll', [
    pytest.param(
        [[1001, 1003], [ ], [1002], [1000, 1005], [1006, 1004]],
        id='as_in_fixture'
    ),
    pytest.param(
        [[1001, 1003], [ ], [1002], [1000, 1005], [1006], [1004]],
        id='last_one'
    ),
    pytest.param(
        [[ ], [1001, 1003], [ ], [1002], [1000, 1005], [1006, 1004]],
        id='empty_first'
    ),
])
def test_receive_one_param(obj, pkgidx_result_pairs, dispatcher, dispatcher_poll):
    dispatcher.poll.side_effect = dispatcher_poll

    actual = [ ]
    while len(actual) < len(pkgidx_result_pairs):
        pair = obj.receive_one()
        if pair is None:
            break
        actual.append(pair)
    assert obj.receive_one() is None
    assert sorted(pkgidx_result_pairs) == sorted(actual)

def test_receive_one_then_receive(obj, pkgidx_result_pairs):
    actual = [ ]

    actual.append(obj.receive_one())

    actual.extend(obj.receive())

    assert sorted(pkgidx_result_pairs) == sorted(actual)

def test_receive_one_then_poll(obj, pkgidx_result_pairs):
    actual = [ ]

    actual.append(obj.receive_one())

    actual.extend(obj.poll())
    actual.extend(obj.poll())
    actual.extend(obj.poll())
    actual.extend(obj.poll())

    assert sorted(pkgidx_result_pairs) == sorted(actual)

##__________________________________________________________________||
