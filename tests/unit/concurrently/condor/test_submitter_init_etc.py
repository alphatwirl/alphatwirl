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
from alphatwirl.concurrently.condor.submitter import clusterprocids2clusterids

##__________________________________________________________________||
def test_clusterprocids2clusterids():
    clusterprocids = [
        '3158642.0', '3158642.1', '3158642.2', '3158642.3', '3158643.0',
        '3158643.1', '3158643.2', '3158643.3', '3158644.0', '3158644.1',
        '3158644.2', '3158644.3', '3158645.0', '3158645.1', '3158645.2',
        '3158645.3'
    ]
    expected = ['3158642', '3158643', '3158644', '3158645']
    assert set(expected) == set(clusterprocids2clusterids(clusterprocids))

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
