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
def mock_proc_condor_submit():
    ret =  mock.Mock()
    ret.returncode = 0
    return ret

@pytest.fixture()
def mock_proc_ondor_prio():
    ret = mock.Mock()
    ret.communicate.return_value = ('', '')
    ret.returncode = 0
    return ret

@pytest.fixture()
def mock_pipe(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    monkeypatch.setattr(module.subprocess, 'PIPE', ret)
    return ret

@pytest.fixture()
def mock_popen(monkeypatch, mock_proc_condor_submit, mock_proc_ondor_prio):
    ret = mock.Mock()
    ret.side_effect = [mock_proc_condor_submit, mock_proc_ondor_prio]
    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    monkeypatch.setattr(module.subprocess, 'Popen', ret)
    return ret

@pytest.fixture()
def obj(mock_popen, mock_pipe):
    job_desc_dict = collections.OrderedDict(
        [('request_memory', '250'), ('Universe', 'chocolate')]
    )
    return HTCondorJobSubmitter(job_desc_dict=job_desc_dict)

@pytest.fixture()
def mock_workingarea(tmpdir_factory):
    ret = mock.Mock(spec=WorkingArea)
    ret.path = str(tmpdir_factory.mktemp(''))
    ret.package_relpath.side_effect = ['task_00000', 'task_00001', 'task_00002']
    ret.executable = 'run.py'
    ret.extra_input_files = set(['python_modules.tar.gz', 'logging_levels.json.gz'])
    return ret

##__________________________________________________________________||
expected_job_desc = textwrap.dedent("""
executable = run.py
output = results/$(resultdir)/stdout.$(cluster).$(process).txt
error = results/$(resultdir)/stderr.$(cluster).$(process).txt
log = results/$(resultdir)/log.$(cluster).$(process).txt
arguments = $(resultdir).p.gz
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = $(resultdir).p.gz, logging_levels.json.gz, python_modules.tar.gz
transfer_output_files = results
universe = chocolate
notification = Error
getenv = True
request_memory = 250
queue resultdir in task_00000, task_00001, task_00002
""").strip()

def test_run_multiple(
        obj, mock_workingarea, mock_popen, mock_pipe,
        mock_proc_condor_submit, caplog):

    obj.clusterprocids_outstanding = ['3764857.0']

    package_indices = [0, 1, 2]
    mock_proc_condor_submit.communicate.return_value = ('3 job(s) submitted to cluster 3764858.', '')

    with caplog.at_level(logging.DEBUG):
        ret = obj.run_multiple(
            workingArea=mock_workingarea, package_indices=package_indices)

    # assert 6 == len(caplog.records)

    #
    assert ['3764858.0', '3764858.1', '3764858.2'] == ret

    #
    assert ['3764857.0', '3764858.0', '3764858.1', '3764858.2'] == obj.clusterprocids_outstanding

    #
    expected = [
        mock.call(
            ['condor_submit'],
            stdin=mock_pipe, stdout=mock_pipe, stderr=mock_pipe,
            cwd=mock_workingarea.path, encoding='utf-8'),
        mock.call(
            ['condor_prio', '-p', '10', '3764858'],
            stdin=mock_pipe, stdout=mock_pipe, stderr=mock_pipe,
            cwd=None, encoding='utf-8'),
    ]
    assert expected == mock_popen.call_args_list

    #
    assert [mock.call(expected_job_desc)] == mock_proc_condor_submit.communicate.call_args_list


def test_run_multiple_empty(
        obj, mock_workingarea, mock_popen,
        mock_proc_condor_submit, caplog):

    obj.clusterprocids_outstanding = ['3764857.0']

    package_indices = [ ]

    with caplog.at_level(logging.DEBUG):
        clusterprocids = obj.run_multiple(
            workingArea=mock_workingarea,
            package_indices=package_indices
        )

    # assert 6 == len(caplog.records)

    #
    assert ['3764857.0'] == obj.clusterprocids_outstanding

    #
    assert [ ] == mock_proc_condor_submit.communicate.call_args_list

    #
    expected = [ ]
    assert expected == clusterprocids

    #
    expected = [ ]
    procargs_list = [args[0] for args, kwargs in mock_popen.call_args_list]
    assert expected == procargs_list

##__________________________________________________________________||
@pytest.fixture()
def mock_run_multiple(monkeypatch, obj):
    ret = mock.Mock()
    ret.return_value = ['3764858.0']
    monkeypatch.setattr(obj, 'run_multiple', ret)
    return ret

def test_run(obj, mock_run_multiple, mock_workingarea):
    assert '3764858.0' == obj.run(workingArea=mock_workingarea, package_index=0)
    expected = [mock.call(mock_workingarea, [0])]
    assert expected == mock_run_multiple.call_args_list

##__________________________________________________________________||
