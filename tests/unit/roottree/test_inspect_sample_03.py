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
    input_file_name = 'sample_03.root'
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
        {'compression_factor': 7.472972972972973,
         'countname': None,
         'isarray': '0',
         'name': 'bChar',
         'size': 7.05718994140625e-05,
         'title': 'bChar/B',
         'type': 'Char_t',
         'uncompressed_size': 0.0005273818969726562},
        {'compression_factor': 7.44,
         'countname': None,
         'isarray': '0',
         'name': 'bUChar',
         'size': 7.152557373046875e-05,
         'title': 'bUChar/b',
         'type': 'UChar_t',
         'uncompressed_size': 0.0005321502685546875},
        {'compression_factor': 7.298701298701299,
         'countname': None,
         'isarray': '0',
         'name': 'bShort',
         'size': 7.343292236328125e-05,
         'title': 'bShort/S',
         'type': 'Short_t',
         'uncompressed_size': 0.0005359649658203125},
        {'compression_factor': 7.269230769230769,
         'countname': None,
         'isarray': '0',
         'name': 'bUShort',
         'size': 7.43865966796875e-05,
         'title': 'bUShort/s',
         'type': 'UShort_t',
         'uncompressed_size': 0.0005407333374023438},
        {'compression_factor': 7.0886075949367084,
         'countname': None,
         'isarray': '0',
         'name': 'bInt',
         'size': 7.534027099609375e-05,
         'title': 'bInt/I',
         'type': 'Int_t',
         'uncompressed_size': 0.0005340576171875},
        {'compression_factor': 7.0625,
         'countname': None,
         'isarray': '0',
         'name': 'bUInt',
         'size': 7.62939453125e-05,
         'title': 'bUInt/i',
         'type': 'UInt_t',
         'uncompressed_size': 0.0005388259887695312},
        {'compression_factor': 7.037037037037037,
         'countname': None,
         'isarray': '0',
         'name': 'bFloat',
         'size': 7.724761962890625e-05,
         'title': 'bFloat/F',
         'type': 'Float_t',
         'uncompressed_size': 0.0005435943603515625},
        {'compression_factor': 6.566666666666666,
         'countname': None,
         'isarray': '0',
         'name': 'bDouble',
         'size': 8.58306884765625e-05,
         'title': 'bDouble/D',
         'type': 'Double_t',
         'uncompressed_size': 0.0005636215209960938},
        {'compression_factor': 6.566666666666666,
         'countname': None,
         'isarray': '0',
         'name': 'bLong64',
         'size': 8.58306884765625e-05,
         'title': 'bLong64/L',
         'type': 'Long64_t',
         'uncompressed_size': 0.0005636215209960938},
        {'compression_factor': 6.549450549450549,
         'countname': None,
         'isarray': '0',
         'name': 'bULong64',
         'size': 8.678436279296875e-05,
         'title': 'bULong64/l',
         'type': 'ULong64_t',
         'uncompressed_size': 0.000568389892578125},
        {'compression_factor': 7.472972972972973,
         'countname': None,
         'isarray': '0',
         'name': 'bBool',
         'size': 7.05718994140625e-05,
         'title': 'bBool/O',
         'type': 'Bool_t',
         'uncompressed_size': 0.0005273818969726562}]}

##__________________________________________________________________||
