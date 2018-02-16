# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

from alphatwirl.roottree import EventBuilderConfig

if not has_no_ROOT:
    from alphatwirl.roottree.BEventBuilder import BEventBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def mockroot(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.roottree.BEventBuilder']
    monkeypatch.setattr(module, 'ROOT', ret)
    return ret

@pytest.fixture()
def mockevents(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.roottree.BEventBuilder']
    monkeypatch.setattr(module, 'BEvents', ret)
    return ret

@pytest.fixture()
def obj(mockroot, mockevents):
    config = EventBuilderConfig(
        inputPaths=['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root'],
        treeName='tree',
        maxEvents=123,
        start=11,
        name='TTJets'
    )
    return BEventBuilder(config)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_build(obj, mockroot, mockevents):
    events = obj()
    assert [mock.call('tree')] == mockroot.TChain.call_args_list
    chain = mockroot.TChain()
    assert [mock.call('/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root')] == chain.Add.call_args_list
    assert [mock.call(chain, 123, 11)] == mockevents.call_args_list

##__________________________________________________________________||
