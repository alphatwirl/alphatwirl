# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import All, Any, Not
from alphatwirl.selection.modules import AllwCount, AnywCount, NotwCount

##__________________________________________________________________||
all_classes = [All, AllwCount]
all_classe_ids = [c.__name__ for c in all_classes]

any_classes = [Any, AnywCount]
any_classe_ids = [c.__name__ for c in any_classes]

not_classes = [Not, NotwCount]
not_classe_ids = [c.__name__ for c in not_classes]

##__________________________________________________________________||
allany_classes = all_classes + any_classes
allany_classe_ids = all_classe_ids + any_classe_ids

##__________________________________________________________________||
@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_init(Class):
    obj = Class()
    assert obj.name is not None
    obj = Class(name='name_of_object')
    assert obj.name is not None
    obj = Class(name=None)
    assert obj.name is not None

    sel1 = mock.sentinel.sel1
    sel2 = mock.sentinel.sel2
    obj = Class(selections=(sel1, sel2))
    assert [sel1, sel2] == obj.selections

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_init(Class):
    sel1 = mock.Mock()
    obj = Class(sel1)
    assert obj.name is not None
    obj = Class(sel1, name='name_of_object')
    assert obj.name is not None
    obj = Class(sel1, name=None)
    assert obj.name is not None

##__________________________________________________________________||
@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_repr(Class):
    obj = Class()
    repr(obj)
    obj = Class(name='name_of_object')
    repr(obj)

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_repr(Class):
    sel1 = mock.Mock()
    obj = Class(sel1)
    repr(obj)
    obj = Class(sel1, name='name_of_object')
    repr(obj)

##__________________________________________________________________||
@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all_call(Class):
    sel1 = mock.Mock()
    sel2 = mock.Mock()

    obj = Class()
    obj.add(sel1)
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

    sel1.assert_called_with(event)
    sel2.assert_called_with(event)

    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any_call(Class):
    sel1 = mock.Mock()
    sel2 = mock.Mock()

    obj = Class()
    obj.add(sel1)
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

    sel1.assert_called_with(event)
    sel2.assert_called_with(event)

    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all_call_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert obj(event)
    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any_call_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert not obj(event)
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_call(Class):
    sel1 = mock.Mock()
    sel1.side_effect = [True, False]

    obj = Class(sel1)

    event = mock.Mock()

    obj.begin(event)

    assert not obj(event)
    assert obj(event)

    sel1.assert_called_with(event)

    obj.end()

##__________________________________________________________________||
