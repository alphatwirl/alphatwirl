# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import logging
import textwrap
import collections

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import WorkingArea
from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
@pytest.fixture()
def mock_proc_condor_q():
    ret =  mock.Mock()
    ret.returncode = 0
    return ret

@pytest.fixture()
def mock_pipe(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module.subprocess, 'PIPE', ret)

    return ret

@pytest.fixture()
def mock_popen(monkeypatch, mock_proc_condor_q):
    ret = mock.Mock()
    ret.side_effect = [mock_proc_condor_q]
    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module.subprocess, 'Popen', ret)
    return ret

@pytest.fixture()
def obj(mock_popen):
    return HTCondorJobSubmitter()

##__________________________________________________________________||
def test_poll(
        obj, mock_popen, mock_pipe,
        mock_proc_condor_q, caplog):

    obj.clusterprocids_outstanding = ['3764857.0', '3764858.0', '3764858.1', '3764858.2']

    stdout = '\n'.join(['3764857.0 2', '3764858.1 2', '3764858.2 1'])
    mock_proc_condor_q.communicate.return_value = (stdout, '')

    with caplog.at_level(logging.DEBUG):
        ret = obj.poll()

    # assert 6 == len(caplog.records)

    #
    assert ['3764857.0', '3764858.1', '3764858.2'] == obj.clusterprocids_outstanding

    #
    expected = ['3764858.0']
    assert expected == ret

    #
    expected = [
        ['condor_q', '3764857', '3764858', '-format', '%d.', 'ClusterId', '-format', '%d ', 'ProcId', '-format', '%-2s\n', 'JobStatus']
    ]
    procargs_list = [args[0] for args, kwargs in mock_popen.call_args_list]
    assert expected == procargs_list

##__________________________________________________________________||
