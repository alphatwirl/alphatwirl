# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently.exec_util import try_executing_until_succeed

##__________________________________________________________________||
def test_without_monkeypatch_subproces():
    procargs = ['ls']
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
    proc.communicate.return_value = ('aaa bbb', '')
    proc.returncode = 0
    subprocess.Popen.side_effect = [proc]

    assert ['aaa bbb'] == try_executing_until_succeed(procargs)

def test_fail_success(subprocess):
    procargs = ['ls']

    proc0 = mock.MagicMock(name='ls')
    proc0.communicate.return_value = ('', '')
    proc0.returncode = 1

    proc1 = mock.MagicMock(name='ls')
    proc1.communicate.return_value = ('aaa bbb', '')
    proc1.returncode = 0

    subprocess.Popen.side_effect = [proc0, proc1]

    assert ['aaa bbb'] == try_executing_until_succeed(procargs)

##__________________________________________________________________||
