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

from alphatwirl.concurrently import HTCondorJobSubmitter

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return HTCondorJobSubmitter()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
@pytest.fixture()
def mock_poll(monkeypatch, obj):
    def ret():
        if len(obj.clusterprocids_outstanding) >= 4:
            obj.clusterprocids_finished.extend(obj.clusterprocids_outstanding[0:2])
            obj.clusterprocids_outstanding[:] = obj.clusterprocids_outstanding[2:]
        else:
            obj.clusterprocids_finished.extend(obj.clusterprocids_outstanding)
            obj.clusterprocids_outstanding[:] = [ ]
    ret.side_effect = ret
    monkeypatch.setattr(obj, 'poll', ret)
    return ret

def test_wait(obj, mock_poll):
    obj.clusterprocids_outstanding = ['3764857.0', '3764858.0', '3764858.1', '3764858.2']
    ret = obj.wait()
    assert [ ] == obj.clusterprocids_outstanding
    assert ['3764857.0', '3764858.0', '3764858.1', '3764858.2'] == ret

##__________________________________________________________________||
def test_failed_runids(obj):
    obj.clusterprocids_finished = ['3764857.0', '3764858.0', '3764858.1', '3764858.2']
    ret = obj.failed_runids(['3764858.1', '3764858.2', '3764858.1', '3764858.3'])
    assert ['3764857.0', '3764858.0'] == obj.clusterprocids_finished

##__________________________________________________________________||
