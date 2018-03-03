# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import numpy as np
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.summary import Summarizer
from alphatwirl.summary import Sum

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return Summarizer(Summary=Sum)

def test_repr(obj):
    repr(obj)

def test_add(obj):

    obj.add('A', (12, ) )
    expected  = {'A': Sum(contents=np.array((12, )))}
    assert expected == obj.results()

    obj.add('A', (23, ))
    expected  = {'A': Sum(contents=np.array((35, )))}
    assert expected == obj.results()

    obj.add('A', (10, ), weight=2)
    expected  = {'A': Sum(contents=np.array((55, )))}
    assert expected == obj.results()

    obj.add('B', (20, ), weight=3.2)
    expected  = {
        'A': Sum(contents=np.array((55, ))),
        'B': Sum(contents=np.array((64.0, ))),
    }
    assert expected == obj.results()

def test_add_key(obj):

    obj.add_key('A')
    expected  = {'A': Sum(contents=np.array((0, )))}
    assert expected == obj.results()

    obj.add_key('B')
    obj.add_key('C')
    expected  = {
        'A': Sum(contents=np.array((0, ))),
        'B': Sum(contents=np.array((0, ))),
        'C': Sum(contents=np.array((0, ))),
    }
    assert expected == obj.results()

def test_key(obj):
    obj.add_key('A')
    assert ['A'] == list(obj.keys())

def test_to_tuple_list(obj):
    obj.add(('A', ), (12, ))
    obj.add(('B', ), (20, ))
    assert [('A', 12), ('B', 20)] == obj.to_tuple_list()

@pytest.mark.skipif(sys.version_info >= (3, 0), reason="requires python 2")
def test_to_tuple_list_key_not_tuple(obj):
    obj.add('A', (12, )) # the keys are not a tuple
    obj.add(2, (20, ))   #
    assert [(2, 20), ('A', 12)] == obj.to_tuple_list()

##__________________________________________________________________||
