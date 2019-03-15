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
    ret =  mock.Mock(name='submit')
    ret.communicate.return_value = (b'3 job(s) submitted to cluster 3764858.', b'')
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

    module = sys.modules['alphatwirl.concurrently.HTCondorJobSubmitter']
    monkeypatch.setattr(module.subprocess, 'PIPE', ret)

    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module.subprocess, 'PIPE', ret)

    return ret

@pytest.fixture()
def mock_popen(monkeypatch, mock_proc_condor_submit, mock_proc_ondor_prio):
    ret = mock.Mock()
    ret.side_effect = [mock_proc_condor_submit, mock_proc_ondor_prio]

    module = sys.modules['alphatwirl.concurrently.HTCondorJobSubmitter']
    monkeypatch.setattr(module.subprocess, 'Popen', ret)

    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module.subprocess, 'Popen', ret)

    return ret

@pytest.fixture()
def obj(mock_popen):
    job_desc_dict = collections.OrderedDict(
        [('request_memory', '250'), ('Universe', 'chocolate')]
    )
    return HTCondorJobSubmitter(job_desc_dict=job_desc_dict)

@pytest.fixture()
def mock_workingarea(tmpdir_factory):
    ret = mock.Mock(spec=WorkingArea)
    ret.path = str(tmpdir_factory.mktemp(''))
    ret.package_path.side_effect = ['task_00000', 'task_00001', 'task_00002']
    ret.executable = 'run.py'
    ret.extra_input_files = set(['python_modules.tar.gz', 'logging_levels.json.gz'])
    return ret

def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
def test_run_multiple(
        obj, mock_workingarea,
        mock_popen, mock_pipe,
        mock_proc_condor_submit, caplog):

    package_indices = [0, 1, 2]

    with caplog.at_level(logging.DEBUG):
        clusterprocids = obj.run_multiple(
            workingArea=mock_workingarea,
            package_indices=package_indices
        )

    # assert 6 == len(caplog.records)

    expected = ['3764858.0', '3764858.1', '3764858.2']
    assert expected == clusterprocids

    expected = [
        mock.call(['condor_submit'], stderr=mock_pipe, stdin=mock_pipe, stdout=mock_pipe),
        mock.call(['condor_prio', '-p', '10', '3764858'], stderr=mock_pipe, stdout=mock_pipe)
    ]
    assert expected == mock_popen.call_args_list

    expected = textwrap.dedent("""
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

    assert [mock.call(expected)] == mock_proc_condor_submit.communicate.call_args_list

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
