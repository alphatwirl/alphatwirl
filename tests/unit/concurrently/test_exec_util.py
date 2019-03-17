# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently.exec_util import try_executing_until_succeed, exec_command, compose_shortened_command_for_logging

##__________________________________________________________________||
params = [
    pytest.param(
        ['echo', 'abc\ndef'], None,
        ['abc', 'def'], # shouldn't be [b'abc', b'def']
        id='simple'
    ),
    pytest.param(
        ['echo'], None,
        [''],
        id='empty-line'
    ),
    pytest.param(
        ['sleep', '0.01'], None,
        [],
        id='empty-output'
    ),
    pytest.param(
        ['cat'], 'abc',
        ['abc'],
        id='stdin'
    ),
]

@pytest.mark.parametrize('procargs, input_, expected', params)
def test_try_executing_until_succeed(procargs, input_, expected):
    stdout = try_executing_until_succeed(procargs, input_=input_)
    assert expected == stdout

@pytest.mark.parametrize('procargs, input_, expected', params)
def test_exec_command(procargs, input_, expected):
    stdout = exec_command(procargs, input_=input_)
    assert expected == stdout

thisdir =  os.path.dirname(os.path.realpath(__file__))

params = [
    pytest.param(['false'], None, '', id='false'),
    pytest.param([os.path.join(thisdir, 'echoerr'), 'error message'], None, 'error message', id='stderr'),
]
@pytest.mark.parametrize('procargs, input_, expected', params)
def test_exec_command_raise(procargs, input_, expected):
    with pytest.raises(RuntimeError) as einfo:
        exec_command(procargs, input_=input_)
    assert expected in str(einfo.value)

##__________________________________________________________________||
def test_try_executing_until_succeed_cwd(tmpdir):
    org_dir = os.getcwd()
    procargs = ['pwd']
    stdout = try_executing_until_succeed(procargs, cwd=str(tmpdir))
    assert [str(tmpdir)] == stdout # shouldn't be [b'abc']
    assert org_dir == os.getcwd()

def test_exec_command_cwd(tmpdir):
    org_dir = os.getcwd()
    procargs = ['pwd']
    stdout = exec_command(procargs, cwd=str(tmpdir))
    assert [str(tmpdir)] == stdout # shouldn't be [b'abc']
    assert org_dir == os.getcwd()

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
    proc.communicate.return_value = ('aaa bbb', '')
    proc.returncode = 0
    subprocess.Popen.side_effect = [proc]

    assert ['aaa bbb'] == try_executing_until_succeed(procargs)

def test_fail_success(subprocess, caplog):
    procargs = ['ls']

    proc0 = mock.MagicMock(name='ls')
    proc0.communicate.return_value = ('', '')
    proc0.returncode = 1

    proc1 = mock.MagicMock(name='ls')
    proc1.communicate.return_value = ('aaa bbb', '')
    proc1.returncode = 0

    subprocess.Popen.side_effect = [proc0, proc1]

    with caplog.at_level(logging.WARNING):
        assert ['aaa bbb'] == try_executing_until_succeed(procargs, sleep=0.1)

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert 'exec_util' in caplog.records[0].name
    assert 'the command failed' in caplog.records[0].msg
    assert caplog.records[1].levelname == 'WARNING'
    assert 'exec_util' in caplog.records[1].name
    assert 'will try again' in caplog.records[1].msg

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
