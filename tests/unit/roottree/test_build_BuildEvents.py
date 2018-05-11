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
    from alphatwirl.roottree import BuildEvents

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def mockroot(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.roottree.build']
    monkeypatch.setattr(module, 'ROOT', ret)
    return ret

@pytest.fixture()
def mockevents(monkeypatch):
    ret = mock.Mock()
    return ret

@pytest.fixture()
def mocktfile():
    ret = mock.Mock()
    ret.good = True
    ret.IsZombie.return_value = False
    return ret

@pytest.fixture()
def mocktfile_null():
    ret = mock.Mock()
    ret.good = False
    ret.GetName.side_effect = ReferenceError
    return ret

@pytest.fixture()
def mocktfile_zombie():
    ret = mock.Mock()
    ret.good = False
    ret.IsZombie.return_value = True
    return ret

@pytest.fixture(
    params=[
        ['good', 'good'],
        ['null', 'good'],
        ['zombie', 'good'],
    ]
)
def files(request, mocktfile, mocktfile_null, mocktfile_zombie):
    map_ = dict(good=mocktfile, null=mocktfile_null, zombie=mocktfile_zombie)
    ret = [map_[p] for p in request.param]
    return ret

@pytest.fixture()
def config(mockevents):
    return dict(
        events_class=mockevents,
        file_paths=['/path/to/input1/tree.root', '/path/to/input2/tree.root'],
        tree_name='tree',
        max_events=123,
        start=11,
        check_files=True,
        skip_error_files=True
    )

@pytest.fixture()
def obj(config, mockroot):
    return BuildEvents(config)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_build(config, files, mockroot, mockevents):
    config['check_files'] = False
    obj = BuildEvents(config)
    mockroot.TFile.Open.side_effect = files
    events = obj()
    assert [mock.call('tree')] == mockroot.TChain.call_args_list
    chain = mockroot.TChain()
    assert [
        mock.call('/path/to/input1/tree.root'),
        mock.call('/path/to/input2/tree.root'),
    ] == chain.Add.call_args_list
    assert [mock.call(chain, 123, 11)] == mockevents.call_args_list

def test_build_skip(config, files, mockroot, mockevents, caplog):
    config['check_files'] = True
    config['skip_error_files'] = True
    obj = BuildEvents(config)
    mockroot.TFile.Open.side_effect = files
    with caplog.at_level(logging.WARNING):
        events = obj()
    assert [mock.call('tree')] == mockroot.TChain.call_args_list
    chain = mockroot.TChain()
    file_paths = [p for p, f in zip(config['file_paths'], files) if f.good]
    assert [mock.call(p) for p in file_paths] == chain.Add.call_args_list
    assert [mock.call(chain, 123, 11)] == mockevents.call_args_list

    assert len(caplog.records) == sum([not f.good for f in files])

    if all([f.good for f in files]):
        return

    assert caplog.records[0].levelname == 'WARNING'
    assert 'cannot open' in caplog.records[0].msg

def test_build_raise(config, files, mockroot, caplog):
    config['check_files'] = True
    config['skip_error_files'] = False
    obj = BuildEvents(config)
    mockroot.TFile.Open.side_effect = files
    if all([f.good for f in files]):
        return

    with caplog.at_level(logging.WARNING):
        with pytest.raises(OSError):
            events = obj()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    assert 'cannot open' in caplog.records[0].msg

##__________________________________________________________________||
