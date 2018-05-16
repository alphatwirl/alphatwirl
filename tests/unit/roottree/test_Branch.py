# Tai Sakuma <tai.sakuma@gmail.com>
import array

import pytest

from alphatwirl.roottree import Branch

##__________________________________________________________________||
def test_repr():
    ar = array.array('d', [112.4, 87.6, 30.2])
    ca = array.array('i', [2])
    obj = Branch('jet_pt', ar, ca)
    repr(obj)

def test_array():
    ar = array.array('d', [112.4, 87.6, 30.2])
    ca = array.array('i', [2])
    obj = Branch('jet_pt', ar, ca)

    assert 2 == len(obj)
    assert 112.4 == obj[0]
    assert 87.6 == obj[1]
    with pytest.raises(IndexError):
        obj[2]

def test_value():
    ar = array.array('d', [112.4])
    ca = None
    obj = Branch('met_pt', ar, ca)

    assert 1 == len(obj)
    assert 112.4 == obj[0]
    with pytest.raises(IndexError):
        obj[1]

##__________________________________________________________________||
