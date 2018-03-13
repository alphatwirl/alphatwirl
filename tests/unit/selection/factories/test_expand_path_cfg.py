# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import pytest

from alphatwirl.selection.factories.FactoryDispatcher import expand_path_cfg

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, expected', [
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
def test_expand_path_cfg(path_cfg, expected):
    actual = expand_path_cfg(path_cfg=path_cfg)
    assert expected == actual

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, error', [
    pytest.param(
        dict(All=(), Any=()), ValueError, id='multiple-vertices-All-Any'
    ),
    pytest.param(
        dict(All=(), Not=()), ValueError, id='multiple-vertices-All-Not'
    ),
    pytest.param(
        dict(Any=(), Not=()), ValueError, id='multiple-vertices-Any-Not'
    ),
    pytest.param(
        dict(), ValueError, id='empty-dict'
    ),
])
def test_expand_path_cfg_raise(path_cfg, error):
    with pytest.raises(error):
        expand_path_cfg(path_cfg=path_cfg)

##__________________________________________________________________||
