# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently.condor.exec_util import try_executing_until_succeed, exec_command, compose_shortened_command_for_logging

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
def test_exec_command(procargs, input_, expected):
    stdout = exec_command(procargs, input_=input_)
    assert expected == stdout

##__________________________________________________________________||
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
def test_exec_command_cwd(tmpdir):
    org_dir = os.getcwd()
    procargs = ['pwd']
    stdout = exec_command(procargs, cwd=str(tmpdir))
    assert [str(tmpdir)] == stdout
    assert org_dir == os.getcwd()

##__________________________________________________________________||
@pytest.fixture()
def mock_exec_command(monkeypatch):
    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    ret = mock.Mock()
    monkeypatch.setattr(module, 'exec_command', ret)
    return ret

@pytest.fixture()
def mock_sleep(monkeypatch):
    module = sys.modules['alphatwirl.concurrently.condor.exec_util']
    ret = mock.Mock()
    monkeypatch.setattr(module.time, 'sleep', ret)
    return ret

@pytest.mark.parametrize('nfails', [0, 1, 5])
def test_try_executing_until_succeed(
        nfails, mock_exec_command, mock_sleep, caplog):
    procargs = mock.sentinel.procargs
    input_ = mock.sentinel.input_
    cwd = mock.sentinel.cwd

    sleep = 0.01

    ret = mock.sentinel.ret

    mock_exec_command.side_effect = [RuntimeError]*nfails + [ret]

    with caplog.at_level(logging.WARNING):
        assert ret == try_executing_until_succeed(
            procargs=procargs, input_=input_, cwd=cwd, sleep=sleep)

    call_exec_command = mock.call(procargs=procargs, input_=input_, cwd=cwd)
    assert [call_exec_command]*(nfails+1) == mock_exec_command.call_args_list

    call_sleep = mock.call(sleep)
    assert [call_sleep]*nfails == mock_sleep.call_args_list

    assert len(caplog.records) == nfails
    for r in caplog.records:
        assert r.levelname == 'WARNING'
        assert 'exec_util' in r.name
        assert 'will try again' in r.msg

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
