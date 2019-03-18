# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
import pytest
from collections import deque

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import TaskPackageDropbox
from alphatwirl.concurrently import WorkingArea, HTCondorJobSubmitter

##__________________________________________________________________||
packages = [
        mock.Mock(name='package0'),
        mock.Mock(name='package1'),
        mock.Mock(name='package2'),
        mock.Mock(name='package3'),
        mock.Mock(name='package4'),
]

results = ['result0', 'result1', 'result2', 'result3', 'result4']

@pytest.fixture()
def collect_results():
    ret = {i: deque([r]) for i, r in enumerate(results)}
    # e.g., {0: deque([result0]), 1:deque([result1]), ...}

    # 3rd job fails twice before succeed
    ret[2].extendleft([None, None])
    # e.g., deque([None, None, result2])

    return ret

@pytest.fixture()
def mock_workingarea(collect_results):
    ret = mock.Mock(spec=WorkingArea)
    ret.put_package.side_effect = [0, 1, 2, 3, 4] # package indices
    ret.collect_result.side_effect = lambda i: collect_results[i].popleft()
    return ret

@pytest.fixture()
def mock_dispatcher():
    ret = mock.Mock(spec=HTCondorJobSubmitter)
    ret.run_multiple.return_value = [1000, 1001, 1002, 1003, 1004]

    # for resubmission
    ret.run.side_effect = [1005, 1006]

    return ret

@pytest.fixture()
def mock_sleep(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.concurrently.TaskPackageDropbox']
    monkeypatch.setattr(module.time, 'sleep', ret)
    return ret

@pytest.fixture()
def obj(mock_workingarea, mock_dispatcher, mock_sleep):
    ret = TaskPackageDropbox(
        workingArea=mock_workingarea,
        dispatcher=mock_dispatcher, sleep=0.01)
    ret.open()
    ret.put_multiple(packages)
    yield ret
    ret.close()

@pytest.fixture()
def expected():
    # e.g., [(0, result0), (1, result1), ...]
    return list(enumerate(results))

##__________________________________________________________________||
params_dispatcher_poll = [
    pytest.param(
        [[1001, 1003], [ ], [1002], [1000, 1005], [1006, 1004]],
        id='example1'
    ),
    pytest.param(
        [[1000, 1001, 1002, 1003, 1004], [1005], [1006]],
        id='example2'
    ),
    pytest.param(
        [[1001, 1003], [ ], [1002], [1000, 1005], [1006], [1004]],
        id='last_one'
    ),
    pytest.param(
        [[ ], [1001, 1003], [ ], [1002], [1000, 1005], [1006, 1004]],
        id='empty_first'
    ),
]

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_receive_one(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    while len(actual) < len(expected):
        actual.append(obj.receive_one())
    assert obj.receive_one() is None
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list
    nmaxsleeps = len(dispatcher_poll)-1
    assert nmaxsleeps >= len(mock_sleep.call_args_list)

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_receive(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    assert expected == obj.receive()
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list
    nsleeps = len(dispatcher_poll)-1
    assert [mock.call(0.01)]*nsleeps == mock_sleep.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_poll(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    while len(actual) < len(expected):
        actual.extend(obj.poll())
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list
    assert [ ] == mock_sleep.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_poll_receive(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    actual.extend(obj.poll())
    actual.extend(obj.receive())
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_receive_one_receive(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    actual.append(obj.receive_one())
    actual.extend(obj.receive())
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_receive_one_poll(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    actual.append(obj.receive_one())
    while len(actual) < len(expected):
        actual.extend(obj.poll())
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_poll_receive_one(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    actual.extend(obj.poll())
    while len(actual) < len(expected):
        actual.append(obj.receive_one())
    assert obj.receive_one() is None
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list

@pytest.mark.parametrize('dispatcher_poll', params_dispatcher_poll)
def test_receive_one_poll_receive(obj, mock_sleep, expected, mock_dispatcher, dispatcher_poll):
    mock_dispatcher.poll.side_effect = dispatcher_poll
    actual = [ ]
    actual.append(obj.receive_one())
    actual.extend(obj.poll())
    actual.extend(obj.receive())
    assert sorted(expected) == sorted(actual)
    assert [mock.call([1002]), mock.call([1005])] == mock_dispatcher.failed_runids.call_args_list

# ##__________________________________________________________________||
def test_receive_logging_resubmission(obj, mock_sleep, mock_dispatcher, caplog):
    mock_dispatcher.poll.side_effect = [[1001, 1003], [ ], [1002], [1000, 1005], [1006, 1004]]
    with caplog.at_level(logging.WARNING):
        obj.receive()
    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[1].levelname == 'WARNING'
    assert 'TaskPackageDropbox' in caplog.records[0].name
    assert 'TaskPackageDropbox' in caplog.records[1].name
    assert 'resubmitting' in caplog.records[0].msg
    assert 'resubmitting' in caplog.records[1].msg

##__________________________________________________________________||
