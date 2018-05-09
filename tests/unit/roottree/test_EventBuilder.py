# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
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


if not has_no_ROOT:
    from alphatwirl.roottree import EventBuilderConfig
    from alphatwirl.roottree import EventBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def mockroot(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.roottree.EventBuilder']
    monkeypatch.setattr(module, 'ROOT', ret)
    return ret

@pytest.fixture()
def mockevents(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.roottree.BEventBuilder']
    monkeypatch.setattr(module, 'BEvents', ret)
    module = sys.modules['alphatwirl.roottree.EventBuilder']
    monkeypatch.setattr(module, 'Events', ret)
    return ret

@pytest.fixture()
def mocktfile():
    ret = mock.Mock()
    ret.IsZombie.return_value = False
    return ret

@pytest.fixture()
def mocktfile_null():
    ret = mock.Mock()
    ret.GetName.side_effect = ReferenceError
    return ret

@pytest.fixture()
def mocktfile_zombie():
    ret = mock.Mock()
    ret.IsZombie.return_value = True
    return ret

@pytest.fixture()
def obj(request, mockroot, mockevents):
    config = EventBuilderConfig(
        inputPaths=['/path/to/input1/tree.root', '/path/to/input2/tree.root'],
        treeName='tree',
        maxEvents=123,
        start=11,
        name='TTJets'
    )
    return EventBuilder(config, EventsClass=mockevents)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_build(obj, mockroot, mocktfile, mockevents):
    mockroot.TFile.Open.return_value = mocktfile
    events = obj()
    assert [mock.call('tree')] == mockroot.TChain.call_args_list
    chain = mockroot.TChain()
    assert [
        mock.call('/path/to/input1/tree.root'),
        mock.call('/path/to/input2/tree.root'),
    ] == chain.Add.call_args_list
    assert [mock.call(chain, 123, 11)] == mockevents.call_args_list

def test_build_raise_null_file(obj, mockroot, mocktfile_null, caplog):
    mockroot.TFile.Open.return_value = mocktfile_null
    with caplog.at_level(logging.WARNING):
        with pytest.raises(OSError):
            events = obj()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    ## assert 'BEventBuilder' in caplog.records[0].name
    assert 'cannot open' in caplog.records[0].msg

def test_build_raise_zombie_file(obj, mockroot, mocktfile_zombie, caplog):
    mockroot.TFile.Open.return_value = mocktfile_zombie
    with caplog.at_level(logging.WARNING):
        with pytest.raises(OSError):
            events = obj()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    ## assert 'BEventBuilder' in caplog.records[0].name
    assert 'cannot open' in caplog.records[0].msg

##__________________________________________________________________||
