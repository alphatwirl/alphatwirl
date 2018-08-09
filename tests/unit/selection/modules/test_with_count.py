# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import AllwCount, AnywCount, NotwCount

##__________________________________________________________________||
@pytest.mark.parametrize('Class', [AllwCount, AnywCount],
                         ids=[AllwCount.__name__, AnywCount.__name__])
def test_allany_init_collector(Class):
    obj = Class()
    assert obj.collector is None
    col = mock.sentinel.col
    obj = Class(collector=col)
    assert obj.collector is col

def test_not_init_collector():
    sel = mock.Mock()
    obj = NotwCount(selection=sel)
    assert obj.collector is None
    col = mock.sentinel.col
    obj = NotwCount(selection=sel, collector=col)
    assert obj.collector is col

##__________________________________________________________________||
class MockEventSelection(object):
    def begin(self, event): pass
    def __call__(self, event): pass
    def end(self): pass

##__________________________________________________________________||
@pytest.mark.parametrize('method', [1, 2, 3])
def test_all(method):
    sel1 = mock.Mock(spec=MockEventSelection)
    sel2 = mock.Mock(spec=MockEventSelection)
    sel1.name ='sel1'
    sel2.name =''

    if method == 1:
        obj = AllwCount()
        obj.add(sel1)
        obj.add(sel2)
    elif method == 2:
        obj = AllwCount(selections=[sel1, sel2])
    elif method == 3:
        obj = AllwCount(selections=[sel1])
        obj.add(sel2)

    event = mock.Mock()

    obj.begin(event)

    # need to set return_value each time because a selection is not
    # guaranteed to be called

    sel1.return_value = True
    sel2.return_value = True
    assert obj(event)

    sel1.return_value = True
    sel2.return_value = False
    assert not obj(event)

    sel1.return_value = False
    sel2.return_value = True
    assert not obj(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj(event)

    obj.end()

    count = obj.results()
    assert [
            [1, 'MockEventSelection', 'sel1', 2, 5],
            [1, 'MockEventSelection',     '', 1, 2],
    ] == count._results

##__________________________________________________________________||
@pytest.mark.parametrize('method', [1, 2, 3])
def test_any(method):
    sel1 = mock.Mock(spec=MockEventSelection)
    sel2 = mock.Mock(spec=MockEventSelection)
    sel1.name ='sel1'
    sel2.name =''

    if method == 1:
        obj = AnywCount()
        obj.add(sel1)
        obj.add(sel2)
    elif method == 2:
        obj = AnywCount(selections=[sel1, sel2])
    elif method == 3:
        obj = AnywCount(selections=[sel1])
        obj.add(sel2)

    event = mock.Mock()

    obj.begin(event)

    # need to set return_value each time because a selection is not
    # guaranteed to be called

    sel1.return_value = True
    sel2.return_value = True
    assert obj(event)

    sel1.return_value = True
    sel2.return_value = False
    assert obj(event)

    sel1.return_value = False
    sel2.return_value = True
    assert obj(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj(event)


    obj.end()

    count = obj.results()
    assert [
            [1, 'MockEventSelection', 'sel1', 2, 5],
            [1, 'MockEventSelection',     '', 1, 3],
    ] == count._results

##__________________________________________________________________||
def test_not():
    sel1 = mock.Mock(spec=MockEventSelection)
    sel1.name ='sel1'

    obj = NotwCount(sel1)

    event = mock.Mock()

    obj.begin(event)

    sel1.return_value = True
    assert not obj(event)

    sel1.return_value = False
    assert obj(event)

    sel1.return_value = False
    assert obj(event)

    obj.end()

    count = obj.results()
    assert [
        [1, 'MockEventSelection', 'sel1', 1, 3],
    ] == count._results

##__________________________________________________________________||
def test_all_empty():
    obj = AllwCount()
    event = mock.Mock()
    obj.begin(event)
    assert obj(event)
    obj.end()
    count = obj.results()
    assert [ ] == count._results

def test_any_empty():
    obj = AnywCount()
    event = mock.Mock()
    obj.begin(event)
    assert not obj(event)
    obj.end()
    count = obj.results()
    assert [ ] == count._results

##__________________________________________________________________||
@pytest.mark.parametrize(
    'Class', [AllwCount, AnywCount],
    ids=[AllwCount.__name__, AnywCount.__name__])
def test_allany_collector(Class):
    obj = Class()
    obj.collect()

    collector = mock.Mock()
    obj = Class(collector=collector)
    result = obj.collect()
    assert [mock.call(obj)] == collector.call_args_list
    assert result is collector()

def test_not_collector():
    sel = mock.Mock()
    obj = NotwCount(selection=sel)
    obj.collect()

    collector = mock.Mock()
    obj = NotwCount(selection=sel, collector=collector)
    result = obj.collect()
    assert [mock.call(obj)] == collector.call_args_list
    assert result is collector()

##__________________________________________________________________||
