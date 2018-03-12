# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.factories.AllFactory import AllFactory

##__________________________________________________________________||
@pytest.fixture()
def MockFactoryDispatcher(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.selection.factories.AllFactory']
    monkeypatch.setattr(module, 'FactoryDispatcher', ret)
    return ret

@pytest.fixture()
def MockAll():
    return mock.Mock()

@pytest.mark.parametrize('kwargs, expected', [
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
def test_call(kwargs, expected, MockAll, MockFactoryDispatcher):
    actual = AllFactory(AllClass=MockAll, **kwargs)
    assert [mock.call(**expected)] == MockAll.call_args_list
    assert actual == MockAll()
    assert [
        mock.call(MockFactoryDispatcher()),
        mock.call(MockFactoryDispatcher()),
    ] == MockAll().add.call_args_list

##__________________________________________________________________||
