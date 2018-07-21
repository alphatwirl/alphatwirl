# Tai Sakuma <tai.sakuma@gmail.com>
import os
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree import BEvents as Events
    from alphatwirl.roottree import Branch

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def tree():
    input_file_name = 'sample_01.root'
    tree_name = 'tree'
    input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', input_file_name)

    input_file = ROOT.TFile.Open(input_path)
    yield input_file.Get(tree_name)

@pytest.fixture()
def events(tree):
    yield Events(tree)

def test_branch(tree, events):
    jet_pt = events.jet_pt
    met_pt = events.met_pt
    assert isinstance(jet_pt, Branch)
    assert isinstance(met_pt, Branch)

    assert 0 == len(jet_pt)
    assert 1 == len(met_pt)
    assert 0.0 == met_pt[0]

    _assert_contents(tree, jet_pt, met_pt)
    _assert_contents(tree, jet_pt, met_pt) # assert twice

def test_2_events(tree, events):
    jet_pt = events.jet_pt
    met_pt = events.met_pt
    _assert_contents(tree, jet_pt, met_pt)

    # the 2nd events object from the same tree
    events2 = Events(tree)
    jet_pt2 = events2.jet_pt
    met_pt2 = events2.met_pt
    assert jet_pt is jet_pt2
    assert met_pt is met_pt2
    _assert_contents(tree, jet_pt, met_pt)

def _assert_contents(tree, jet_pt, met_pt):

    tree.GetEntry(0)
    assert 2 == len(jet_pt)
    assert 1 == len(met_pt)
    assert 124.55626678466797 == jet_pt[0]
    assert 86.90544128417969 == jet_pt[1]
    assert 43.783382415771484 == met_pt[0]

    tree.GetEntry(1)
    assert 3 == len(jet_pt)
    assert 1 == len(met_pt)
    assert 112.48554992675781 == jet_pt[0]
    assert 52.32780075073242 == jet_pt[1]
    assert 48.861289978027344 == jet_pt[2]
    assert 20.483951568603516 == met_pt[0]

##__________________________________________________________________||
