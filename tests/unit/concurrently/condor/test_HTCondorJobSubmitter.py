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
def proc_submit():
    ret =  mock.MagicMock(name='proc_condor_submit')
    ret.communicate.return_value = (b'1 job(s) submitted to cluster 1012.', b'')
    return ret

@pytest.fixture()
def proc_prio():
    ret = mock.MagicMock(name='proc_condor_prio')
    ret.communicate.return_value = ('', '')
    ret.returncode = 0
    return ret

@pytest.fixture()
def mocksubprocess(monkeypatch, proc_submit, proc_prio):
    ret = mock.MagicMock(name='subprocess')

    module = sys.modules['alphatwirl.concurrently.HTCondorJobSubmitter']
    monkeypatch.setattr(module, 'subprocess', ret)

    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module, 'subprocess', ret)

    ret.Popen.side_effect = [proc_submit, proc_prio]
    return ret

@pytest.fixture()
def obj(mocksubprocess):
    job_desc_extra = ['request_memory = 900']
    return HTCondorJobSubmitter(job_desc_extra=job_desc_extra)

@pytest.fixture()
def workingarea(tmpdir_factory):
    ret = mock.Mock(spec=WorkingArea)
    ret.path = str(tmpdir_factory.mktemp(''))
    ret.package_path.return_value = 'tpd_20161129_122841_HnpcmF'
    ret.executable = 'run.py'
    ret.extra_input_files = set(['python_modules.tar.gz', 'logging_levels.json.gz'])
    return ret

def test_repr(obj):
    repr(obj)

def test_run(obj, workingarea, proc_submit, caplog):
    with caplog.at_level(logging.WARNING):
        assert '1012.0' == obj.run(workingArea=workingarea, package_index=0)

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
    universe = vanilla
    notification = Error
    getenv = True
    request_memory = 900
    queue resultdir in tpd_20161129_122841_HnpcmF
    """).strip()

    assert [mock.call(expected)] == proc_submit.communicate.call_args_list

##__________________________________________________________________||
def test_option_job_desc_dict(mocksubprocess, workingarea, proc_submit):
    job_desc_dict = collections.OrderedDict(
        [('request_memory', '1200'), ('Universe', 'chocolate')]
    )
    obj = HTCondorJobSubmitter(job_desc_dict=job_desc_dict)
    obj.run(workingArea=workingarea, package_index=0)

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
    request_memory = 1200
    queue resultdir in tpd_20161129_122841_HnpcmF
    """).strip()

    assert [mock.call(expected)] == proc_submit.communicate.call_args_list

##__________________________________________________________________||
