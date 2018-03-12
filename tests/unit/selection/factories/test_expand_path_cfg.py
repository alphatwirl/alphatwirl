# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import pytest

from alphatwirl.selection.factories.FactoryDispatcher import expand_path_cfg

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

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, expected', [
    pytest.param(
        'alias1',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias1'
        ),
        id='alias1'
    ),
    pytest.param(
        ('alias1', dict(name='name1')),
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var1[0] >= 10',
            name='name1'
        ),
        id='alias1:with-name'
    ),
    pytest.param(
        'alias2',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var2[0] >= 20',
            name='name2' #  name has priority over alias
        ),
        id='alias2:name-priority-over-alias'
    ),
    pytest.param(
        ('alias2', dict(name='new_name2')),
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var2[0] >= 20',
            name='new_name2' # name can be overridden
        ),
        id='alias2:name-overridden'
    ),
    pytest.param(
        'alias3',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias3' # the outermost alias has priority
        ),
        id='alias3:alias-of-alias'
    ),
    pytest.param(
        'alias4',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias4' # the outermost alias has priority
        ),
        id='alias4:alias-of-alias-of-alias'
    ),
    pytest.param(
        ('alias5', dict(n=30)),
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.var4[0] == {n}', # not formatted
            n=30,
            name='alias5'
        ),
        id='alias5:not-formatted'
    ),
    pytest.param(
        'alias6',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : {low} <= ev.var5[0] < {high}',
            low=11,
            high=20,
            name='alias6',
        ),
        id='alias6:not-formatted-with-default-values'
    ),
    pytest.param(
        ('alias6', dict(high=30)),
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : {low} <= ev.var5[0] < {high}',
            low=11,
            high=30,
            name='alias6'
        ),
        id='alias6:not-formatted-with-default-values-overridden'
    ),
    pytest.param(
        'ev : ev.nJets[0] >= 2',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.nJets[0] >= 2',
        ),
        id='string:lambda_str'
    ),
    pytest.param(
        'ev : ev.nJets[0] >= {n}',
        dict(
            factory='LambdaStrFactory',
            lambda_str='ev : ev.nJets[0] >= {n}',
        ),
        id='string:lambda_str-not-formatted'
    ),
    pytest.param(
        dict(All=()),
        {'factory': 'AllFactory', 'path_cfg_list': ()},
        id='dict-all-empty'
    ),
    pytest.param(
        dict(Any=()),
        {'factory': 'AnyFactory', 'path_cfg_list': ()},
        id='dict-any-empty'
    ),
    pytest.param(
        dict(All=(dict(factory='factory1'), dict(factory='factory2')), name='test_all', arg2=2, arg3=3),
        dict(
            factory='AllFactory',
            path_cfg_list=(dict(factory='factory1'), dict(factory='factory2')),
            name='test_all',
            arg2=2, arg3=3
        ),
        id='dict-all'
    ),
    pytest.param(
        dict(Any=(dict(factory='factory1'), dict(factory='factory2')), name='test_any', arg2=2, arg3=3),
        dict(
            factory='AnyFactory',
            path_cfg_list=(dict(factory='factory1'), dict(factory='factory2')),
            name='test_any',
            arg2=2, arg3=3
        ),
        id='dict-any'
    ),
    pytest.param(
        dict(Not=dict(factory='factory1'), name='test_not', arg2=2, arg3=3),
        dict(
            factory='NotFactory',
            path_cfg=dict(factory='factory1'),
            name='test_not',
            arg2=2, arg3=3
        ),
        id='dict-not'
    ),
    pytest.param(
        dict(Any=(
            'ev : ev.x[0] == 0',
            dict(All=(
                'ev : ev.x[0] >= 1',
                'ev : ev.y[0] >= 100',
                )),
            dict(Not=dict(
                Any=(
                    'ev : ev.z[0] == 0',
                    'ev : ev.w[0] >= 300',
                ),
            )),
        )),
        {
            'factory': 'AnyFactory',
            'path_cfg_list': (
                {
                    'factory': 'LambdaStrFactory',
                    'lambda_str': 'ev : ev.x[0] == 0',
                },
                {
                    'factory': 'AllFactory',
                    'path_cfg_list': (
                        {
                            'factory': 'LambdaStrFactory',
                            'lambda_str': 'ev : ev.x[0] >= 1',
                        },
                        {
                            'factory': 'LambdaStrFactory',
                            'lambda_str': 'ev : ev.y[0] >= 100',
                        }
                    )
                },
                {
                    'factory': 'NotFactory',
                    'path_cfg': {
                        'factory': 'AnyFactory',
                        'path_cfg_list': (
                            {
                                'factory': 'LambdaStrFactory',
                                'lambda_str': 'ev : ev.z[0] == 0'
                            },
                            {
                                'factory': 'LambdaStrFactory',
                                'lambda_str': 'ev : ev.w[0] >= 300'
                            }
                        )
                    }
                }
            )
        },
        id='example',
        ## marks=pytest.mark.skip(reason='not fully expanded')
    ),
])
def test_expand_path_cfg(alias_dict, path_cfg, expected):
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    assert expected == actual

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, error', [
    pytest.param(
        dict(All=(), Any=()), ValueError, id='multiple vertices: All Any'
    ),
    pytest.param(
        dict(All=(), Not=()), ValueError, id='multiple vertices: All Not'
    ),
    pytest.param(
        dict(Any=(), Not=()), ValueError, id='multiple vertices: Any Not'
    ),
    pytest.param(
        dict(), ValueError, id='empty dict'
    ),
])
def test_expand_path_cfg_raise(path_cfg, error):
    with pytest.raises(error):
        expand_path_cfg(path_cfg=path_cfg)

##__________________________________________________________________||
