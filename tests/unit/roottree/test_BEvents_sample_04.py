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
    input_file_name = 'sample_04.root'
    tree_name = 'tree'
    input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', input_file_name)

    input_file = ROOT.TFile.Open(input_path)
    yield input_file.Get(tree_name)

@pytest.fixture()
def events(tree):
    yield Events(tree)

def test_event(events):

    event = events[0]
    assert [-125, 38] == list(event.bChar)
    assert [253, 20] == list(event.bUChar)
    assert [-10, 120] == list(event.bShort)
    assert [65530, 21221] == list(event.bUShort)
    assert [-2147483626, 512] == list(event.bInt)
    assert [4294967290, 1253] == list(event.bUInt)
    assert [-0.123, 42.344] == pytest.approx(list(event.bFloat), rel=1e-6)
    assert [-2.345, 51.224] == list(event.bDouble)
    assert [-4611686018427387900, 12345] == list(event.bLong64)
    assert [9223372036854775802, 12345514] == list(event.bULong64)
    assert [1, 1] == list(event.bBool)

##__________________________________________________________________||
