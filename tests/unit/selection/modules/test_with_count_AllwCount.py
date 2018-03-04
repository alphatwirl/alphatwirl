# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import AllwCount

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return AllwCount()

def test_repr(obj):
    repr(obj)

def test_empty(obj):

    event = mock.Mock()
    obj.begin(event)

    event = mock.Mock()
    assert obj(event)

    count = obj.results()
    assert [ ] == count._results

def test_standard(obj):
    sel1 = mock.Mock()
    sel1.name ='sel1'
    sel1.__class__.__name__ = 'MockEventSelection'
    del sel1.results

    sel2 = mock.Mock()
    sel2.name =''
    sel2.__class__.__name__ = 'MockEventSelection'
    del sel2.results

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
    sel2.return_value = True   # 1/1
    assert obj(event)

    event = mock.Mock()
    sel1.return_value = True   # 2/2
    sel2.return_value = False  # 1/2
    assert not obj(event)

    event = mock.Mock()
    sel1.return_value = False  # 2/3
    sel2.return_value = True   # 1/2
    assert not obj(event)

    event = mock.Mock()
    sel1.ret = False  # 2/4
    sel2.ret = False  # 1/2
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
    # all (obj) --- all (obj1) --- sel (sel11)
    #            |              +- sel (sel12)
    #            +- all (obj2) --- sel (sel21)
    #            |              +- sel (sel22)
    #            +- sel (sel3)
    #
    obj1 = AllwCount('all1')
    obj2 = AllwCount('all2')

    sel11 = mock.Mock()
    sel11.name ='sel11'
    sel11.__class__.__name__ = 'MockEventSelection'
    del sel11.results

    sel12 = mock.Mock()
    sel12.name ='sel12'
    sel12.__class__.__name__ = 'MockEventSelection'
    del sel12.results

    sel21 = mock.Mock()
    sel21.name ='sel21'
    sel21.__class__.__name__ = 'MockEventSelection'
    del sel21.results

    sel22 = mock.Mock()
    sel22.name ='sel22'
    sel22.__class__.__name__ = 'MockEventSelection'
    del sel22.results

    sel3 = mock.Mock()
    sel3.name ='sel3'
    sel3.__class__.__name__ = 'MockEventSelection'
    del sel3.results

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
        [1, 'AllwCount', 'all1',  1, 1],
        [2, 'MockEventSelection',     'sel11', 1, 1],
        [2, 'MockEventSelection',     'sel12', 1, 1],
        [1, 'AllwCount', 'all2',  1, 1],
        [2, 'MockEventSelection',     'sel21', 1, 1],
        [2, 'MockEventSelection',     'sel22', 1, 1],
        [1, 'MockEventSelection',     'sel3',  1, 1],
    ] == count._results

##__________________________________________________________________||
