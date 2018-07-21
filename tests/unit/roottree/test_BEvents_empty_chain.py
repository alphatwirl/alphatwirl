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
def chain():
    tree_name = 'tree'
    chain = ROOT.TChain(tree_name)
    # add no files to the chain
    yield chain

@pytest.fixture()
def events(chain):
    yield Events(chain)

def test_access_branch_raise(events):
    with pytest.raises(AttributeError):
        events.var

##__________________________________________________________________||
