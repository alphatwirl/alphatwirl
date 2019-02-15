# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import CommunicationChannel0
from alphatwirl.progressbar import atpbar
import alphatwirl

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def global_variables(monkeypatch):
    monkeypatch.setattr(alphatwirl.progressbar, 'do_not_start_monitor', False)
    monkeypatch.setattr(alphatwirl.progressbar, '_reporter', None)
    monkeypatch.setattr(alphatwirl.progressbar, '_monitor', None)

##__________________________________________________________________||
def task_atpbar(*args, **kwargs):
   for i in atpbar(range(100), name='task'):
      pass
   return

##__________________________________________________________________||
def test_progressbar_on(capsys):
    obj = CommunicationChannel0(progressbar=True)
    obj.begin()
    obj.put(task_atpbar)
    obj.receive()
    obj.end()
    alphatwirl.progressbar._end_monitor()

    captured = capsys.readouterr()
    assert ('        0 /      100 (  0.00%) task' in captured.out)

def test_progressbar_off(capsys):
    obj = CommunicationChannel0(progressbar=False)
    obj.begin()
    obj.put(task_atpbar)
    obj.receive()
    obj.end()
    alphatwirl.progressbar._end_monitor()

    captured = capsys.readouterr()
    assert '' == captured.out

##__________________________________________________________________||
