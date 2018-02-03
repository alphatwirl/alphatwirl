# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently.exec_util import try_executing_until_succeed, compose_shortened_command_for_logging

##__________________________________________________________________||
def test_without_monkeypatch_subproces(caplog):
    procargs = ['ls']
    with caplog.at_level(logging.DEBUG, logger = 'alphatwirl'):
        try_executing_until_succeed(procargs)

##__________________________________________________________________||
@pytest.fixture()
def subprocess(monkeypatch):
    module = sys.modules['alphatwirl.concurrently.exec_util']
    ret = mock.MagicMock(name='subprocess')
    monkeypatch.setattr(module, 'subprocess', ret)
    return ret

def test_success(subprocess):
    procargs = ['ls']

    proc = mock.MagicMock(name='ls')
    proc.communicate.return_value = (b'aaa bbb', b'')
    proc.returncode = 0
    subprocess.Popen.side_effect = [proc]

    assert [b'aaa bbb'] == try_executing_until_succeed(procargs)

def test_fail_success(subprocess, caplog):
    procargs = ['ls']

    proc0 = mock.MagicMock(name='ls')
    proc0.communicate.return_value = (b'', b'')
    proc0.returncode = 1

    proc1 = mock.MagicMock(name='ls')
    proc1.communicate.return_value = (b'aaa bbb', b'')
    proc1.returncode = 0

    subprocess.Popen.side_effect = [proc0, proc1]

    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        assert [b'aaa bbb'] == try_executing_until_succeed(procargs, sleep=0.1)

##__________________________________________________________________||
def test_compose_shortened_command_for_logging():
    procargs = ['condor_q', '3158110', '3158111', '3158112', '3158113',
                '3158114', '3158115', '3158116', '3158117', '3158118', '3158119',
                '3158120', '3158121', '3158122', '3158123', '3158124', '3158125',
                '-format', '%-2s ', 'ClusterId', '-format', '%-2s\n', 'JobStatus']
    expected = 'condor_q 3158110 3158111 3158112 3158113 3158114 3...((86 letters))... -format "%-2s " ClusterId -format %-2s\n JobStatus'
    actual = compose_shortened_command_for_logging(procargs)
    assert expected == actual

##__________________________________________________________________||
