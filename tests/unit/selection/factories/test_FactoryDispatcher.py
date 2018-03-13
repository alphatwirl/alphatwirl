# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.selection.factories.factory import FactoryDispatcher
from alphatwirl.selection.modules.LambdaStr import LambdaStr
from alphatwirl.selection.modules import All, Any, Not

##__________________________________________________________________||
alias_dict = {
    'alias1': 'ev : ev.var1[0] >= 10',
    'alias2': ('ev : ev.var2[0] >= 20', dict(name='name2')),
    'alias3': 'alias1',
    'alias4': 'alias3',
    'alias5': 'ev : ev.var4[0] == {n}',
    'alias6': ('ev : {low} <= ev.var5[0] < {high}', dict(low=11, high=20))
}

##__________________________________________________________________||
params = [
    pytest.param(
        dict(Any=(
            'ev : ev.x[0] == 0',
            dict(All=(
                'ev : ev.x[0] >= 1',
                'ev : ev.y[0] >= 100',
                'alias4',
                )),
            dict(Not=dict(
                Any=(
                    'ev : ev.z[0] == 0',
                    'ev : ev.w[0] >= 300',
                    'alias5',
                    'alias6',
                ),
            )),
        )),
        dict(
            AllClass=All, AnyClass=Any, NotClass=Not,
            LambdaStrClass=LambdaStr, aliasDict=alias_dict,
            n=5242,
        ),
        Any(selections=[
            LambdaStr('ev : ev.x[0] == 0'),
            All(selections=[
                LambdaStr('ev : ev.x[0] >= 1'),
                LambdaStr('ev : ev.y[0] >= 100'),
                LambdaStr(name='alias4', lambda_str='ev : ev.var1[0] >= 10'),
            ]),
            Not(selection=Any(selections=[
                LambdaStr('ev : ev.z[0] == 0'),
                LambdaStr('ev : ev.w[0] >= 300'),
                LambdaStr(name='alias5', lambda_str='ev : ev.var4[0] == 5242'),
                LambdaStr(name='alias6', lambda_str='ev : 11 <= ev.var5[0] < 20'),
            ]),
            ),
        ]),
        id='example'
    ),
]

@pytest.mark.parametrize('path_cfg, kargs, expected', params)
def test_dispatcher(path_cfg, kargs, expected):
    obj = FactoryDispatcher(path_cfg=path_cfg, **kargs)
    assert repr(expected) == repr(obj)
    assert str(expected) == str(obj)

##__________________________________________________________________||
