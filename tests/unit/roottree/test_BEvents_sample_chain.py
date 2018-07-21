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
    input_file_names = [
        'sample_chain_01.root',
        'sample_chain_02.root',
        'sample_chain_03.root',
    ]
    input_paths = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', n)
        for n in input_file_names
    ]
    tree_name = 'tree'
    chain = ROOT.TChain(tree_name)
    for p in input_paths:
        chain.Add(p)
    yield chain

@pytest.fixture()
def events(chain):
    yield Events(chain)

def test_event(events):

    content_list = [
        # file 1
        [10, 20, 30],
        [24, 5],

        # file 2
        [3, 10],
        [5, 8, 32, 15, 2],
        [22, 11],

        # file 3
        [2, 7],
        [10, 100],
    ]

    for i, c in enumerate(content_list):
        event = events[i]
        assert len(c) == event.nvar[0]
        assert c == list(event.var)

##__________________________________________________________________||
