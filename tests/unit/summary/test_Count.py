# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np
import copy

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.summary import Count

##__________________________________________________________________||
@pytest.mark.parametrize('kwargs, expected_contents', (
    (dict(), [np.array([0, 0])]),
    (dict(val=()), [np.array([1, 1])]),
    (dict(val=(), weight=10), [np.array([10, 100])]),
    (dict(contents=[np.array([1, 3])]), [np.array([1, 3])]),
))
def test_init(kwargs, expected_contents):
    obj = Count(**kwargs)
    np.testing.assert_equal(expected_contents, obj.contents)

##__________________________________________________________________||
def test_repr():
    obj = Count()
    repr(obj)

##__________________________________________________________________||
def test_add():
    obj1 = Count(contents=[np.array((10, 20))])
    obj2 = Count(contents=[np.array((30, 40))])
    obj3 =  obj1 + obj2
    np.testing.assert_equal([np.array([40, 60])], obj3.contents)
    assert obj1 is not obj3
    assert obj1.contents is not obj3.contents
    assert obj2 is not obj3
    assert obj2.contents is not obj3.contents

def test_radd():
    obj1 = Count(contents=[np.array((10, 20))])
    assert obj1 is not sum([obj1]) # will call 0 + obj1
    assert obj1 == sum([obj1])

def test_radd_raise():
    obj1 = Count(contents=[np.array((10, 20))])
    with pytest.raises(TypeError):
        1 + obj1

def test_copy():
    obj1 = Count(contents=[np.array((10, 20))])
    copy1 = copy.copy(obj1)
    assert obj1 == copy1
    assert obj1 is not copy1
    assert obj1.contents is not copy1.contents
    assert obj1.contents[0] is not copy1.contents[0]

##__________________________________________________________________||
