# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import All, Any, Not
from alphatwirl.selection.modules import AllwCount, AnywCount, NotwCount

##__________________________________________________________________||
allany_classes = [All, AllwCount, Any, AnywCount]
allany_classe_ids = [c.__name__ for c in allany_classes]

@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_begin(Class):
    obj = Class()
    sel1 = mock.Mock()
    sel2 = mock.Mock()
    del sel2.begin
    obj.add(sel1)
    obj.add(sel2)
    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == sel1.begin.call_args_list

@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_end(Class):
    obj = Class()
    sel1 = mock.Mock()
    sel2 = mock.Mock()
    del sel2.end
    obj.add(sel1)
    obj.add(sel2)
    obj.end()
    assert [mock.call()] == sel1.end.call_args_list

##__________________________________________________________________||
not_classes = [Not, NotwCount]
not_classe_ids = [c.__name__ for c in not_classes]

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_begin(Class):
    selection = mock.Mock()
    obj = Class(selection)
    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == selection.begin.call_args_list

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_begin_absent(Class):
    selection = mock.Mock()
    del selection.begin
    obj = Class(selection)
    event = mock.Mock()
    obj.begin(event)

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_end(Class):
    selection = mock.Mock()
    obj = Class(selection)
    obj.end()
    assert [mock.call()] == selection.end.call_args_list

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_end_absent(Class):
    selection = mock.Mock()
    del selection.end
    obj = Class(selection)
    obj.end()

##__________________________________________________________________||
