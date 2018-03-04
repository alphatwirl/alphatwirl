# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import NotwCount

##__________________________________________________________________||
class MockEventSelection(object):
    def begin(self, event): pass
    def __call__(self, event): pass
    def end(self): pass

@pytest.fixture()
def sel1():
    ret = mock.Mock(spec=MockEventSelection)
    ret.name ='sel1'
    sel1.return_value = True
    return ret

@pytest.fixture()
def obj(sel1):
    return NotwCount(selection=sel1)

def test_repr(obj):
    repr(obj)

def test_standard(obj, sel1):

    assert [ ] == sel1.begin.call_args_list
    assert [ ] == sel1.end.call_args_list


    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == sel1.begin.call_args_list

    event = mock.Mock()
    sel1.return_value = False   # 1/1
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = True   # 1/2
    assert not obj(event)

    obj.end()
    assert [mock.call()] == sel1.end.call_args_list

    count = obj.results()
    assert [
        [1, 'MockEventSelection', 'sel1', 1, 2],
    ] == count._results

##__________________________________________________________________||
def test_nested(sel1):

    obj1 = NotwCount(selection=sel1)
    obj = NotwCount(selection=obj1)

    assert [ ] == sel1.begin.call_args_list
    assert [ ] == sel1.end.call_args_list

    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == sel1.begin.call_args_list

    event = mock.Mock()
    sel1.return_value = False   # 0/1
    assert not obj(event)

    event = mock.Mock()
    sel1.return_value = True   # 1/2
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = True   # 2/3
    assert obj(event)

    obj.end()
    assert [mock.call()] == sel1.end.call_args_list

    count = obj.results()
    print count._results
    assert [
        [1, 'NotwCount', 'Not', 1, 3],
        [2, 'MockEventSelection', 'sel1', 2, 3],
    ] == count._results

##__________________________________________________________________||
