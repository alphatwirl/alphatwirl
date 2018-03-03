# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import copy
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
def obj1():
    ret = Summarizer(Summary=Sum)
    ret._results.update({
        (1, ): Sum(contents=np.array((4, ))),
        (2, ): Sum(contents=np.array((3, ))),
        (3, ): Sum(contents=np.array((2, ))),
    })
    return ret

@pytest.fixture()
def obj2():
    ret = Summarizer(Summary=Sum)
    ret._results.update({
        (2, ): Sum(contents=np.array((3.2, ))),
        (4, ): Sum(contents=np.array((2, ))),
    })
    return ret

@pytest.fixture()
def expected():
    return {
        (1, ): Sum(contents=np.array((4, ))),
        (2, ): Sum(contents=np.array((6.2, ))),
        (3, ): Sum(contents=np.array((2, ))),
        (4, ): Sum(contents=np.array((2, ))),
    }

def test_add(obj1, obj2, expected):
    obj3 = obj1 + obj2
    assert expected == obj3._results
    assert obj1._results[(1, )] is not obj3._results[(1, )]
    assert obj2._results[(4, )] is not obj3._results[(4, )]

def test_radd(obj1, obj2, expected):
    obj3 = sum([obj1, obj2]) # 0 + obj1 is executed
    assert expected == obj3._results
    assert obj1._results[(1, )] is not obj3._results[(1, )]
    assert obj2._results[(4, )] is not obj3._results[(4, )]

def test_iadd(obj1, obj2, expected):
    obj3 = obj1

    obj3 += obj2
    assert obj3 is obj1
    assert expected == obj3._results

def test_copy(obj1):
    copy1 = copy.copy(obj1)
    assert obj1._results == copy1._results
    assert obj1._results[(1, )]is not copy1._results[(1, )]
    assert obj1._results[(2, )]is not copy1._results[(2, )]
    assert obj1._results[(3, )]is not copy1._results[(3, )]

##__________________________________________________________________||
