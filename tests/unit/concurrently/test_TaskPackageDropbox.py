# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import TaskPackageDropbox

##__________________________________________________________________||
@pytest.fixture()
def workingarea():
    return mock.MagicMock()

@pytest.fixture()
def dispatcher():
    return mock.MagicMock()

@pytest.fixture()
def obj(workingarea, dispatcher):
    return TaskPackageDropbox(workingArea=workingarea, dispatcher=dispatcher, sleep=0.01)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_open_terminate_close(obj, workingarea, dispatcher):

    assert 0 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 0 == dispatcher.terminate.call_count

    obj.open()
    assert 1 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 0 == dispatcher.terminate.call_count

    obj.terminate()
    assert 1 == workingarea.open.call_count
    assert 0 == workingarea.close.call_count
    assert 1 == dispatcher.terminate.call_count

    obj.close()
    assert 1 == workingarea.open.call_count
    assert 1 == workingarea.close.call_count
    assert 1 == dispatcher.terminate.call_count

def test_put(obj, workingarea, dispatcher):

    ## open
    obj.open()

    ## put
    workingarea.put_package.side_effect = [0, 1] # pkgidx
    dispatcher.run.side_effect = [1001, 1002] # runid

    package0 = mock.MagicMock(name='package0')
    obj.put(package0)

    package1 = mock.MagicMock(name='package1')
    obj.put(package1)

    assert [mock.call(package0), mock.call(package1)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, 0), mock.call(workingarea, 1)] == dispatcher.run.call_args_list

def test_put_multiple(obj, workingarea, dispatcher):

    ## open
    obj.open()

    ## put
    workingarea.put_package.side_effect = [0, 1] # pkgidx
    dispatcher.run_multiple.return_value = [1001, 1002] # runid

    package0 = mock.MagicMock(name='package0')
    package1 = mock.MagicMock(name='package1')

    obj.put_multiple([package0, package1])

    assert [mock.call(package0), mock.call(package1)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, [0, 1])] == dispatcher.run_multiple.call_args_list

def test_receive_all_finished_once(obj, workingarea, dispatcher):

    ## open
    obj.open()

    ## put
    workingarea.put_package.side_effect = [0, 1]
    dispatcher.run.side_effect = [1001, 1002]

    package0 = mock.MagicMock(name='package0')
    obj.put(package0)

    package1 = mock.MagicMock(name='package1')
    obj.put(package1)

    assert [mock.call(package0), mock.call(package1)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, 0), mock.call(workingarea, 1)] == dispatcher.run.call_args_list

    ## receive
    dispatcher.poll.side_effect = [[1001, 1002]]
    result0 = mock.MagicMock(name='result0')
    result1 = mock.MagicMock(name='result1')
    workingarea.collect_result.side_effect = lambda x: {0: result0, 1: result1}[x]

    assert 0 == dispatcher.poll.call_count
    assert [result0, result1] == obj.receive()
    assert 1 == dispatcher.poll.call_count
    assert [mock.call([])] == dispatcher.failed_runids.call_args_list

    ## close
    assert 0 == dispatcher.terminate.call_count
    obj.terminate()
    obj.close()
    assert 1 == dispatcher.terminate.call_count

def test_receive_finished_in_steps(obj, workingarea, dispatcher):

    ## open
    obj.open()

    ## put
    workingarea.put_package.side_effect = [0, 1, 2]
    dispatcher.run.side_effect = [1001, 1002, 1003]

    package0 = mock.MagicMock(name='package0')
    obj.put(package0)

    package1 = mock.MagicMock(name='package1')
    obj.put(package1)

    package2 = mock.MagicMock(name='package2')
    obj.put(package2)

    assert [mock.call(package0), mock.call(package1), mock.call(package2)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, 0), mock.call(workingarea, 1), mock.call(workingarea, 2)] == dispatcher.run.call_args_list

    ## receive
    dispatcher.poll.side_effect = [[1001, 1003], [ ], [1002]]
    result0 = mock.MagicMock(name='result0')
    result1 = mock.MagicMock(name='result1')
    result2 = mock.MagicMock(name='result2')
    workingarea.collect_result.side_effect = lambda x: {0: result0, 1: result1, 2: result2}[x]

    assert 0 == dispatcher.poll.call_count
    assert [result0, result1, result2] == obj.receive()
    assert 3 == dispatcher.poll.call_count

    assert [mock.call([]), mock.call([]), mock.call([])] == dispatcher.failed_runids.call_args_list

    ## close
    assert 0 == dispatcher.terminate.call_count
    obj.terminate()
    obj.close()
    assert 1 == dispatcher.terminate.call_count

def test_receive_rerun(obj, workingarea, dispatcher, caplog):

    ## open
    obj.open()

    ## put
    workingarea.put_package.side_effect = [0, 1, 2]
    dispatcher.run.side_effect = [1001, 1002, 1003]

    package0 = mock.MagicMock(name='package0')
    obj.put(package0)

    package1 = mock.MagicMock(name='package1')
    obj.put(package1)

    package2 = mock.MagicMock(name='package2')
    obj.put(package2)

    assert [mock.call(package0), mock.call(package1), mock.call(package2)] == workingarea.put_package.call_args_list
    assert [mock.call(workingarea, 0), mock.call(workingarea, 1), mock.call(workingarea, 2)] == dispatcher.run.call_args_list

    ## receive
    dispatcher.poll.side_effect = [[1001, 1003], [ ], [1002, 1004], [1005]]
    dispatcher.run.side_effect = [1004, 1005]
    result0 = mock.MagicMock(name='result0')
    result1 = mock.MagicMock(name='result1')
    result2 = mock.MagicMock(name='result2')

    return_result0 = mock.MagicMock(side_effect=[result0])
    return_result1 = mock.MagicMock(side_effect=[result1])
    return_result2 = mock.MagicMock(side_effect=[None, None, result2]) # fail twice before success
    workingarea.collect_result.side_effect = lambda x : {
        0: return_result0,
        1: return_result1,
        2: return_result2,
    }[x]()

    assert 0 == dispatcher.poll.call_count
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        received = obj.receive()

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[1].levelname == 'WARNING'
    assert 'TaskPackageDropbox' in caplog.records[0].name
    assert 'TaskPackageDropbox' in caplog.records[1].name
    assert 'resubmitting' in caplog.records[0].msg
    assert 'resubmitting' in caplog.records[1].msg

    assert [result0, result1, result2] == received
    assert 4 == dispatcher.poll.call_count

    assert [mock.call([1003]), mock.call([]), mock.call([1004]), mock.call([])] == dispatcher.failed_runids.call_args_list

    ## close
    assert 0 == dispatcher.terminate.call_count
    obj.terminate()
    obj.close()
    assert 1 == dispatcher.terminate.call_count

##__________________________________________________________________||
