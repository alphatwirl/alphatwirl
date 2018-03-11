# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import pytest

from alphatwirl.selection.factories.FactoryDispatcher import FactoryDispatcher
from alphatwirl.selection.modules.LambdaStr import LambdaStr

##__________________________________________________________________||
@pytest.fixture()
def alias_dict():
    return {
        'alias1': 'ev : ev.var1[0] >= 10',
        'alias2': ('ev : ev.var2[0] >= 20', dict(name='name2')),
        'alias3': 'alias1',
        'alias4': 'alias3',
        'alias5': 'ev : ev.var4[0] == {n}',
        'alias6': ('ev : {low} <= ev.var5[0] < {high}', dict(low=11, high=20))
    }

@pytest.fixture()
def sys_path(monkeypatch):
    two_up_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    monkeypatch.syspath_prepend(two_up_dir)

##__________________________________________________________________||
def test_string(sys_path, alias_dict):
    kargs = dict(
        arg1=10, arg2=20,
        aliasDict=alias_dict,
        LambdaStrClass=LambdaStr
    )
    path_cfg = 'alias1'
    obj = FactoryDispatcher(path_cfg=path_cfg, **kargs)
    assert isinstance(obj, LambdaStr)
    assert 'alias1' == obj.name
    assert 'ev : ev.var1[0] >= 10' == obj.lambda_str

##__________________________________________________________________||
