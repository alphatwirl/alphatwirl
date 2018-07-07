# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
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
@pytest.fixture()
def mocksel():
    ret = mock.MagicMock()
    ret.__str__.return_value = '\n'.join(['Mocksel:', '    line1', '    line2'])
    return ret

##__________________________________________________________________||
@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_str(Class, mocksel):
    obj1 = Class(selections=[mocksel, mocksel])
    obj0 = Class(selections=[obj1])
    str(obj1)
    str(obj0)

##__________________________________________________________________||
