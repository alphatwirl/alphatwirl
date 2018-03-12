# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.factories.AllFactory import AllFactory
from alphatwirl.selection.factories.AnyFactory import AnyFactory
from alphatwirl.selection.factories.NotFactory import NotFactory

##__________________________________________________________________||
@pytest.fixture()
def MockFactoryDispatcher(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.selection.factories.AllFactory']
    monkeypatch.setattr(module, 'FactoryDispatcher', ret)
    module = sys.modules['alphatwirl.selection.factories.AnyFactory']
    monkeypatch.setattr(module, 'FactoryDispatcher', ret)
    module = sys.modules['alphatwirl.selection.factories.NotFactory']
    monkeypatch.setattr(module, 'FactoryDispatcher', ret)
    return ret

@pytest.mark.parametrize('kwargs, expected_kwargs', [
    pytest.param(
        dict(
            path_cfg_list = ("ev : ev.nJet[0] >= 2", "ev : ev.nMET[0] >= 200"),
            name='test_all',
        ),
        dict(
            name='test_all',
        ),
        id='simple',
    ),
])
def test_AllFactory(kwargs, expected_kwargs, MockFactoryDispatcher):
    MockClass = mock.Mock()
    obj = AllFactory(AllClass=MockClass, **kwargs)
    assert [mock.call(**expected_kwargs)] == MockClass.call_args_list
    assert obj == MockClass()
    assert [
        mock.call(MockFactoryDispatcher()),
        mock.call(MockFactoryDispatcher()),
    ] == MockClass().add.call_args_list

@pytest.mark.parametrize('kwargs, expected_kwargs', [
    pytest.param(
        dict(
            path_cfg_list = ("ev : ev.nJet[0] >= 2", "ev : ev.nMET[0] >= 200"),
            name='test_any',
        ),
        dict(
            name='test_any',
        ),
        id='simple',
    ),
])
def test_AnyFactory(kwargs, expected_kwargs, MockFactoryDispatcher):
    MockClass = mock.Mock()
    obj = AnyFactory(AnyClass=MockClass, **kwargs)
    assert [mock.call(**expected_kwargs)] == MockClass.call_args_list
    assert obj == MockClass()
    assert [
        mock.call(MockFactoryDispatcher()),
        mock.call(MockFactoryDispatcher()),
    ] == MockClass().add.call_args_list

@pytest.mark.parametrize('kwargs, expected_kwargs', [
    pytest.param(
        dict(
            path_cfg = "ev : ev.nJet[0] >= 2",
            name='test_not',
        ),
        dict(
            name='test_not',
        ),
        id='simple',
    ),
])
def test_NotFactory(kwargs, expected_kwargs, MockFactoryDispatcher):
    MockClass = mock.Mock()
    obj = NotFactory(NotClass=MockClass, **kwargs)
    expected_kwargs['selection'] = MockFactoryDispatcher()
    assert [mock.call(**expected_kwargs)] == MockClass.call_args_list
    assert obj == MockClass()

##__________________________________________________________________||
