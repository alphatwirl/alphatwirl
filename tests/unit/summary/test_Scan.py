# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np
import copy

import pytest

from alphatwirl.summary import Scan

##__________________________________________________________________||
@pytest.mark.parametrize('kwargs, expected_contents', (
    (dict(), [ ]),
    (dict(val=(10, 20)), [(10, 20)]),
    (dict(val=(10, 20), weight=2), [(10, 20)]),
    (dict(contents=[(10, 20), (30, 40)]), [(10, 20), (30, 40)]),
))
def test_init(kwargs, expected_contents):
    obj = Scan(**kwargs)
    np.testing.assert_equal(expected_contents, obj.contents)

##__________________________________________________________________||
@pytest.mark.skip(reason='they can be the same object for now')
def test_init_contents_not_same_object():
    contents = [[10, 20], [30, 40]]
    obj = Scan(contents=contents)
    assert contents is not obj.contents
    assert contents[0] is not obj.contents[0]
    assert contents[1] is not obj.contents[1]

##__________________________________________________________________||
def test_repr():
    obj = Scan()
    repr(obj)

##__________________________________________________________________||
def test_add():
    obj1 = Scan(contents=[(10, 20), (30, 40)])
    obj2 = Scan(contents=[(50, 60), (70, 80)])
    obj3 =  obj1 + obj2
    assert [(10, 20), (30, 40), (50, 60), (70, 80)] == obj3.contents
    assert obj1 is not obj3
    assert obj1.contents is not obj3.contents
    assert obj2 is not obj3
    assert obj2.contents is not obj3.contents

def test_radd():
    obj1 = Scan(contents=[(10, 20), (30, 40)])
    assert obj1 is not sum([obj1]) # will call 0 + obj1
    assert obj1 == sum([obj1])

def test_radd_raise():
    obj1 = Scan(contents=[(10, 20), (30, 40)])
    with pytest.raises(TypeError):
        1 + obj1

##__________________________________________________________________||
def test_copy():
    obj1 = Scan(contents=[(10, 20), (30, 40)])
    copy1 = copy.copy(obj1)
    assert obj1 == copy1
    assert obj1 is not copy1
    assert obj1.contents is not copy1.contents

##__________________________________________________________________||
