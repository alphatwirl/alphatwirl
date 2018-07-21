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
    input_file_name = 'sample_03.root'
    tree_name = 'tree'
    input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', input_file_name)

    input_file = ROOT.TFile.Open(input_path)
    yield input_file.Get(tree_name)

@pytest.fixture()
def events(tree):
    yield Events(tree)

def test_event(events):

    event = events[0]
    assert -125 == event.bChar[0]
    assert 253 == event.bUChar[0]
    assert -10 == event.bShort[0]
    assert 65530 == event.bUShort[0]
    assert -2147483626 == event.bInt[0]
    assert 4294967290 == event.bUInt[0]
    assert -0.123 == pytest.approx(event.bFloat[0], rel=1e-6)
    assert -2.345 == event.bDouble[0]
    assert -4611686018427387900 == event.bLong64[0]
    assert 9223372036854775802 == event.bULong64[0]
    assert 1 == event.bBool[0]

    event = events[1]
    assert 127 == event.bChar[0]
    assert 4 == event.bUChar[0]
    assert 32765 == event.bShort[0]
    assert 8 == event.bUShort[0]
    assert 2147483640 == event.bInt[0]
    assert 12 == event.bUInt[0]
    assert 0.244 == pytest.approx(event.bFloat[0], rel=1e-6)
    assert 3.122 == event.bDouble[0]
    assert 9223372036854775733 == event.bLong64[0]
    assert 123 == event.bULong64[0]
    assert 0 == event.bBool[0]

##__________________________________________________________________||
