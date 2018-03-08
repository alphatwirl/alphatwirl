# Tai Sakuma <tai.sakuma@gmail.com>

# The tests in this file are similar to those in test_selection.py.
# While __call__() is used in test_selection.py, the method event() is
# used in this file.
# The method event() is to be deleted, and so is this test file.
# The __call__() should be used. The selections are not specific to
# events. The method event() is kept for the comparability for now.

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
@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all(Class):
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
    assert obj.event(event)

    sel1.return_value = True
    sel2.return_value = False
    assert not obj.event(event)

    sel1.return_value = False
    sel2.return_value = True
    assert not obj.event(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj.event(event)

    sel1.assert_called_with(event)
    sel2.assert_called_with(event)

    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any(Class):
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
    assert obj.event(event)

    sel1.return_value = True
    sel2.return_value = False
    assert obj.event(event)

    sel1.return_value = False
    sel2.return_value = True
    assert obj.event(event)

    sel1.return_value = False
    sel2.return_value = False
    assert not obj.event(event)

    sel1.assert_called_with(event)
    sel2.assert_called_with(event)

    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert obj.event(event)
    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert not obj.event(event)
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not(Class):
    sel1 = mock.Mock()
    sel1.side_effect = [True, False]

    obj = Class(sel1)

    event = mock.Mock()

    obj.begin(event)

    assert not obj.event(event)
    assert obj.event(event)

    obj.end()

##__________________________________________________________________||
