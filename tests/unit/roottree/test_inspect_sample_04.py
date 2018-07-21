# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import numbers
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree import inspect_tree

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


def test_inspect(tree):
    actual = inspect_tree(tree)

    ## assert expected == actual ## this doesn't work in different
                                 ## architectures.

    assert len(expected) == len(actual) # only 'leaves'
    leaves_expected = expected['leaves']
    leaves_actual = actual['leaves']
    assert len(leaves_expected) == len(leaves_actual)
    for leave_expected, leave_actual in zip(leaves_expected, leaves_actual):
        assert len(leave_expected) == len(leave_actual)
        keys = list(leave_expected.keys())
        for key in keys:
            e = leave_expected[key]
            a = leave_actual[key]
            if isinstance(e, numbers.Integral):
                assert e == a
            elif isinstance(e, numbers.Number):
                assert e == pytest.approx(a, rel=1e-1)
            else:
                assert e == a

expected = {
    'leaves': [
        {'compression_factor': 7.413333333333333,
         'countname': None,
         'isarray': '0',
         'name': 'nvar',
         'size': 7.152557373046875e-05,
         'title': 'nvar/I',
         'type': 'Int_t',
         'uncompressed_size': 0.000530242919921875},
        {'compression_factor': 7.5813953488372094,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bChar',
         'size': 8.20159912109375e-05,
         'title': 'bChar[nvar]/B',
         'type': 'Char_t',
         'uncompressed_size': 0.000621795654296875},
        {'compression_factor': 7.551724137931035,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bUChar',
         'size': 8.296966552734375e-05,
         'title': 'bUChar[nvar]/b',
         'type': 'UChar_t',
         'uncompressed_size': 0.0006265640258789062},
        {'compression_factor': 7.426966292134831,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bShort',
         'size': 8.487701416015625e-05,
         'title': 'bShort[nvar]/S',
         'type': 'Short_t',
         'uncompressed_size': 0.0006303787231445312},
        {'compression_factor': 7.4,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bUShort',
         'size': 8.58306884765625e-05,
         'title': 'bUShort[nvar]/s',
         'type': 'UShort_t',
         'uncompressed_size': 0.0006351470947265625},
        {'compression_factor': 7.164835164835165,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bInt',
         'size': 8.678436279296875e-05,
         'title': 'bInt[nvar]/I',
         'type': 'Int_t',
         'uncompressed_size': 0.000621795654296875},
        {'compression_factor': 7.141304347826087,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bUInt',
         'size': 8.7738037109375e-05,
         'title': 'bUInt[nvar]/i',
         'type': 'UInt_t',
         'uncompressed_size': 0.0006265640258789062},
        {'compression_factor': 7.193548387096774,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bFloat',
         'size': 8.869171142578125e-05,
         'title': 'bFloat[nvar]/F',
         'type': 'Float_t',
         'uncompressed_size': 0.0006380081176757812},
        {'compression_factor': 6.764705882352941,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bDouble',
         'size': 9.72747802734375e-05,
         'title': 'bDouble[nvar]/D',
         'type': 'Double_t',
         'uncompressed_size': 0.0006580352783203125},
        {'compression_factor': 6.764705882352941,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bLong64',
         'size': 9.72747802734375e-05,
         'title': 'bLong64[nvar]/L',
         'type': 'Long64_t',
         'uncompressed_size': 0.0006580352783203125},
        {'compression_factor': 6.747572815533981,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bULong64',
         'size': 9.822845458984375e-05,
         'title': 'bULong64[nvar]/l',
         'type': 'ULong64_t',
         'uncompressed_size': 0.0006628036499023438},
        {'compression_factor': 7.5813953488372094,
         'countname': 'nvar',
         'isarray': '1',
         'name': 'bBool',
         'size': 8.20159912109375e-05,
         'title': 'bBool[nvar]/O',
         'type': 'Bool_t',
         'uncompressed_size': 0.000621795654296875}]}

##__________________________________________________________________||
