# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
@pytest.fixture()
def mock_proc_condor_rm():
    ret =  mock.Mock()
    ret.returncode = 0
    return ret

@pytest.fixture()
def mock_pipe(monkeypatch):
    ret = mock.Mock()

    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    monkeypatch.setattr(module.subprocess, 'PIPE', ret)

    return ret

@pytest.fixture()
def mock_popen(monkeypatch, mock_proc_condor_rm):
    ret = mock.Mock()
    ret.side_effect = [mock_proc_condor_rm]

    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    monkeypatch.setattr(module.subprocess, 'Popen', ret)
    return ret

@pytest.fixture()
def obj(mock_popen):
    return HTCondorJobSubmitter()

##__________________________________________________________________||
def test_terminate(
        obj, mock_popen, mock_pipe,
        mock_proc_condor_rm, caplog):

    obj.clusterprocids_outstanding = ['3764857.0', '3764858.0', '3764858.1', '3764858.2']

    stdout = 'All jobs matching constraint (ClusterId == 3764857 || ClusterId == 3764858) have been marked for removal'
    mock_proc_condor_rm.communicate.return_value = (stdout, '')

    with caplog.at_level(logging.DEBUG):
        ret = obj.terminate()

    # assert 6 == len(caplog.records)

    #
    assert ['3764857.0', '3764858.0', '3764858.1', '3764858.2'] == obj.clusterprocids_outstanding

    #
    assert ret is None

    #
    expected = [
        mock.call(
            ['condor_rm', '3764857', '3764858'],
            stdin=mock_pipe, stdout=mock_pipe, stderr=mock_pipe,
            cwd=None, encoding='utf-8'),
    ]
    assert expected == mock_popen.call_args_list

##__________________________________________________________________||
