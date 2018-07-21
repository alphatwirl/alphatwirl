# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
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
    input_file_name = 'sample_02.root'
    tree_name = 'tree'
    input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', input_file_name)

    input_file = ROOT.TFile.Open(input_path)
    yield input_file.Get(tree_name)

@pytest.fixture()
def events(tree):
    yield Events(tree)

@pytest.mark.skipif(sys.version_info[0]!=2, reason="skip for Python 3")
def test_vector(tree, events):
    trigger_path = events.trigger_path
    trigger_decision = events.trigger_decision

    assert tree.GetEntry(0) > 0
    assert 449 == len(trigger_path)
    assert 'AlCa_EcalEtaEBonly' == trigger_path[0]
    assert 'DST_Physics' == trigger_path[12]
    assert 'HLT_SingleForJet25' == trigger_path[438]
    assert 449 == len(trigger_decision)
    assert 0 == trigger_decision[0]
    assert 0 == trigger_decision[13]
    assert 0 == trigger_decision[438]

    assert tree.GetEntry(1) > 0
    assert 438 == len(trigger_path)
    assert 'AlCa_EcalEtaEBonly' == trigger_path[0]
    assert 'DST_Ele8_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT250' == trigger_path[12]
    with pytest.raises(IndexError):
        trigger_path[438]
    assert 438 == len(trigger_decision)
    assert 0 == trigger_decision[0]
    assert 1 == trigger_decision[13]
    with pytest.raises(IndexError):
        trigger_decision[438]

    # This sample file has only two entries. When the 3rd entry is
    # tried to be accessed, GetEntry(2) returns 0, but the vectors
    # won't be cleared. These have the previous contents.
    assert tree.GetEntry(2) == 0
    assert 438 == len(trigger_path)
    assert 438 == len(trigger_decision)

##__________________________________________________________________||
