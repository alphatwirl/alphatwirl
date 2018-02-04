# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import logging
import textwrap

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
job_desc_template_with_extra = """
Executable = run.py
output = results/$(resultdir)/stdout.txt
error = results/$(resultdir)/stderr.txt
log = results/$(resultdir)/log.txt
Arguments = $(resultdir).p.gz
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = {input_files}
transfer_output_files = results
Universe = vanilla
notification = Error
getenv = True
request_memory = 900
queue resultdir in {resultdirs}
"""
job_desc_template_with_extra = textwrap.dedent(job_desc_template_with_extra).strip()

##__________________________________________________________________||
@pytest.fixture()
def subprocess():
    proc_submit = mock.MagicMock(name='proc_condor_submit')
    proc_submit.communicate.return_value = (b'1 job(s) submitted to cluster 1012.', b'')

    proc_prio = mock.MagicMock(name='proc_condor_prio')
    proc_prio.communicate.return_value = ('', '')
    proc_prio.returncode = 0

    ret = mock.MagicMock(name='subprocess')
    ret.Popen.side_effect = [proc_submit, proc_prio]
    return ret

@pytest.fixture()
def obj(monkeypatch, subprocess):
    module = sys.modules['alphatwirl.concurrently.HTCondorJobSubmitter']
    monkeypatch.setattr(module, 'subprocess', subprocess)
    module = sys.modules['alphatwirl.concurrently.exec_util']
    monkeypatch.setattr(module, 'subprocess', subprocess)
    return HTCondorJobSubmitter()

def test_repr(obj):
    repr(obj)

def test_init_job_desc_extra(obj):
    job_desc_extra = ['request_memory = 900']
    obj = HTCondorJobSubmitter(job_desc_extra=job_desc_extra)
    assert job_desc_template_with_extra == obj.job_desc_template

def test_run(obj, tmpdir_factory, caplog):
    workingarea = mock.MagicMock()
    workingarea.path = str(tmpdir_factory.mktemp(''))
    workingarea.package_path.return_value = 'aaa'
    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        assert '1012.0' == obj.run(workingArea=workingarea, package_index=0)

##__________________________________________________________________||
