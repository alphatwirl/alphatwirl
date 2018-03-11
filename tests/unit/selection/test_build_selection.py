# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection import build_selection
from alphatwirl.selection.modules import All
from alphatwirl.selection.modules import Any
from alphatwirl.selection.modules import Not
from alphatwirl.selection.modules.LambdaStr import LambdaStr

##__________________________________________________________________||
@pytest.fixture()
def MockFactoryDispatcher(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.selection.funcs']
    monkeypatch.setattr(module, 'FactoryDispatcher', ret)
    return ret

def test_call_kargs(MockFactoryDispatcher):

    kargs = dict(
        arg1=10,
        arg2=20,
        level=dict(factory='test_level1', arg2=2, arg3=3)
    )

    obj = build_selection(**kargs)

    assert MockFactoryDispatcher() is obj

    expected = [mock.call(
        AllClass=All, AnyClass=Any, NotClass=Not,
        LambdaStrClass=LambdaStr, aliasDict={ },
        arg1=10, arg2=20, level=dict(factory='test_level1', arg2=2, arg3=3))
    ] == MockFactoryDispatcher.call_args_list

##__________________________________________________________________||
