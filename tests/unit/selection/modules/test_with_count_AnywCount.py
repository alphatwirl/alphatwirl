# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import AnywCount

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return AnywCount()

def test_repr(obj):
    repr(obj)

class MockEventSelection(object):
    def begin(self, event): pass
    def __call__(self, event): pass
    def end(self): pass

def test_empty(obj):

    event = mock.Mock()
    obj.begin(event)

    event = mock.Mock()
    assert not obj(event)

    count = obj.results()
    assert [ ] == count._results

def test_standard(obj):
    sel1 = mock.Mock(spec=MockEventSelection)
    sel1.name ='sel1'

    sel2 = mock.Mock(spec=MockEventSelection)
    sel2.name =''

    obj.add(sel1)
    obj.add(sel2)

    assert [ ] == sel1.begin.call_args_list
    assert [ ] == sel2.begin.call_args_list

    assert [ ] == sel1.end.call_args_list
    assert [ ] == sel2.end.call_args_list


    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == sel1.begin.call_args_list
    assert [mock.call(event)] == sel2.begin.call_args_list

    event = mock.Mock()
    sel1.return_value = True   # 1/1
    sel2.return_value = True   # 0/0
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = True   # 2/2
    sel2.return_value = False  # 0/0
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = False  # 2/3
    sel2.return_value = True   # 1/1
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = False  # 2/4
    sel2.return_value = False  # 1/2
    assert not obj(event)

    obj.end()
    assert [mock.call()] == sel1.end.call_args_list
    assert [mock.call()] == sel2.end.call_args_list

    count = obj.results()
    assert [
            [1, 'MockEventSelection', 'sel1', 2, 4],
            [1, 'MockEventSelection',     '', 1, 2],
    ] == count._results

def test_nested(obj):
    #
    # any (obj) --- any (obj1) --- sel (sel11)
    #            |              +- sel (sel12)
    #            +- any (obj2) --- sel (sel21)
    #            |              +- sel (sel22)
    #            +- sel (sel3)
    #
    obj1 = AnywCount('any1')
    obj2 = AnywCount('any2')

    sel11 = mock.Mock(spec=MockEventSelection)
    sel11.name ='sel11'

    sel12 = mock.Mock(spec=MockEventSelection)
    sel12.name ='sel12'

    sel21 = mock.Mock(spec=MockEventSelection)
    sel21.name ='sel21'

    sel22 = mock.Mock(spec=MockEventSelection)
    sel22.name ='sel22'

    sel3 = mock.Mock(spec=MockEventSelection)
    sel3.name ='sel3'

    obj.add(obj1)
    obj.add(obj2)
    obj.add(sel3)
    obj1.add(sel11)
    obj1.add(sel12)
    obj2.add(sel21)
    obj2.add(sel22)

    assert [ ] == sel11.begin.call_args_list
    assert [ ] == sel12.begin.call_args_list
    assert [ ] == sel21.begin.call_args_list
    assert [ ] == sel22.begin.call_args_list
    assert [ ] == sel3.begin.call_args_list

    assert [ ] == sel11.end.call_args_list
    assert [ ] == sel12.end.call_args_list
    assert [ ] == sel21.end.call_args_list
    assert [ ] == sel22.end.call_args_list
    assert [ ] == sel3.end.call_args_list

    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == sel11.begin.call_args_list
    assert [mock.call(event)] == sel12.begin.call_args_list
    assert [mock.call(event)] == sel21.begin.call_args_list
    assert [mock.call(event)] == sel22.begin.call_args_list
    assert [mock.call(event)] == sel3.begin.call_args_list

    event = mock.Mock()
    sel11.return_value = True   # 1/1
    sel12.return_value = True   # 1/1
    sel21.return_value = True   # 1/1
    sel22.return_value = True   # 1/1
    sel3.return_value = True    # 1/1
    assert obj(event)

    obj.end()
    assert [mock.call()] == sel11.end.call_args_list
    assert [mock.call()] == sel12.end.call_args_list
    assert [mock.call()] == sel21.end.call_args_list
    assert [mock.call()] == sel22.end.call_args_list
    assert [mock.call()] == sel3.end.call_args_list

    count = obj.results()
    assert [
        [1, 'AnywCount', 'any1',  1, 1],
        [2, 'MockEventSelection',     'sel11', 1, 1],
        [2, 'MockEventSelection',     'sel12', 0, 0],
        [1, 'AnywCount', 'any2',  0, 0],
        [2, 'MockEventSelection',     'sel21', 0, 0],
        [2, 'MockEventSelection',     'sel22', 0, 0],
        [1, 'MockEventSelection',     'sel3',  0, 0],
    ] == count._results

##__________________________________________________________________||
def test_merge(obj):
    #
    # any (obj) --- any (obj1) --- sel (sel11)
    #            |              +- sel (sel12)
    #            +- any (obj2) --- sel (sel21)
    #            |              +- sel (sel22)
    #            +- sel (sel3)
    #

    obj.count = mock.MagicMock()
    obj.count.__iadd__.return_value = obj.count

    obj1 = AnywCount('any1')
    obj1.count = mock.MagicMock()
    obj1.count.__iadd__.return_value = obj1.count

    obj2 = AnywCount('any2')
    obj2.count = mock.MagicMock()
    obj2.count.__iadd__.return_value = obj2.count

    sel11 = mock.Mock(spec=MockEventSelection)
    sel11.name ='sel11'

    sel12 = mock.Mock(spec=MockEventSelection)
    sel12.name ='sel12'

    sel21 = mock.Mock(spec=MockEventSelection)
    sel21.name ='sel21'

    sel22 = mock.Mock(spec=MockEventSelection)
    sel22.name ='sel22'

    sel3 = mock.Mock(spec=MockEventSelection)
    sel3.name ='sel3'

    obj.add(obj1)
    obj.add(obj2)
    obj.add(sel3)
    obj1.add(sel11)
    obj1.add(sel12)
    obj2.add(sel21)
    obj2.add(sel22)

    obj_copy = copy.deepcopy(obj)
    obj.merge(obj_copy)

    assert [mock.call(obj_copy.count)] == obj.count.__iadd__.call_args_list
    assert [mock.call(obj_copy.selections[0].count)] == obj1.count.__iadd__.call_args_list
    assert [mock.call(obj_copy.selections[1].count)] == obj2.count.__iadd__.call_args_list

##__________________________________________________________________||
