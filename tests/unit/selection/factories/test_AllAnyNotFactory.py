# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.factories.factory import AllFactory
from alphatwirl.selection.factories.factory import AnyFactory
from alphatwirl.selection.factories.factory import NotFactory

##__________________________________________________________________||
def test_AllFactory():
    MockClass = mock.Mock()
    component1 = mock.sentinel.component1
    component2 = mock.sentinel.component1
    components = (component1, component2)
    name = mock.sentinel.name
    obj = AllFactory(components=components, AllClass=MockClass, name=name)
    assert [mock.call(name=name)] == MockClass.call_args_list
    assert [
        mock.call(component1),
        mock.call(component2),
    ] == MockClass().add.call_args_list

def test_AnyFactory():
    MockClass = mock.Mock()
    component1 = mock.sentinel.component1
    component2 = mock.sentinel.component1
    components = (component1, component2)
    name = mock.sentinel.name
    obj = AnyFactory(components=components, AnyClass=MockClass, name=name)
    assert [mock.call(name=name)] == MockClass.call_args_list
    assert [
        mock.call(component1),
        mock.call(component2),
    ] == MockClass().add.call_args_list

def test_NotFactory():
    MockClass = mock.Mock()
    component1 = mock.sentinel.component1
    components = (component1, )
    name = mock.sentinel.name
    obj = NotFactory(components=components, NotClass=MockClass, name=name)
    assert [mock.call(selection=component1, name=name)] == MockClass.call_args_list
    assert obj == MockClass()


##__________________________________________________________________||
