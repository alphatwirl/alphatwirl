# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import Not, NotwCount

##__________________________________________________________________||
not_classes = [Not, NotwCount]
not_classe_ids = [c.__name__ for c in not_classes]

@pytest.mark.parametrize('NotClass', not_classes, ids=not_classe_ids)
def test_not_begin(NotClass):
    selection = mock.Mock()
    obj = NotClass(selection)
    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == selection.begin.call_args_list

@pytest.mark.parametrize('NotClass', not_classes, ids=not_classe_ids)
def test_not_begin_absent(NotClass):
    selection = mock.Mock()
    del selection.begin
    obj = NotClass(selection)
    event = mock.Mock()
    obj.begin(event)

@pytest.mark.parametrize('NotClass', not_classes, ids=not_classe_ids)
def test_not_end(NotClass):
    selection = mock.Mock()
    obj = NotClass(selection)
    obj.end()
    assert [mock.call()] == selection.end.call_args_list

@pytest.mark.parametrize('NotClass', not_classes, ids=not_classe_ids)
def test_not_end_absent(NotClass):
    selection = mock.Mock()
    del selection.end
    obj = NotClass(selection)
    obj.end()

##__________________________________________________________________||
