# Tai Sakuma <tai.sakuma@gmail.com>
import os
import sys
import pytest

from alphatwirl.selection.factories.expand import expand_path_cfg

from alphatwirl.selection.factories.factory import FactoryDispatcher
from alphatwirl.selection.modules.LambdaStr import LambdaStr
from alphatwirl.selection.modules import All, Any, Not

##__________________________________________________________________||
# path_cfg, expanded, obj
params = [
    pytest.param(
        'ev : ev.nJets[0] >= 2',
        dict(
            components=(),
            factory='LambdaStrFactory',
            lambda_str='ev : ev.nJets[0] >= 2',
        ),
        LambdaStr(
            name='ev : ev.nJets[0] >= 2',
            lambda_str='ev : ev.nJets[0] >= 2',
        ),
        id='string:lambda_str'
    ),
    pytest.param(
        'ev : ev.nJets[0] >= {n}',
        dict(
            components=(),
            factory='LambdaStrFactory',
            lambda_str='ev : ev.nJets[0] >= {n}',
        ),
        LambdaStr(
            name='ev : ev.nJets[0] >= 5242',
            lambda_str='ev : ev.nJets[0] >= 5242',
        ),
        id='string:lambda_str-not-formatted'
    ),
    pytest.param(
        dict(All=()),
        {'factory': 'AllFactory', 'components': ()},
        All(name='All', selections=[]),
        id='dict-all-empty'
    ),
    pytest.param(
        dict(Any=()),
        {'factory': 'AnyFactory', 'components': ()},
        Any(name='Any', selections=[]),
        id='dict-any-empty'
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
        dict(
            factory='AnyFactory',
            components=(
                dict(
                    factory='LambdaStrFactory',
                    components=(),
                    lambda_str='ev : ev.x[0] == 0',
                ),
                dict(
                    factory='AllFactory',
                    components=(
                        dict(
                            factory='LambdaStrFactory',
                            components=(),
                            lambda_str='ev : ev.x[0] >= 1',
                        ),
                        dict(
                            factory='LambdaStrFactory',
                            components=(),
                            lambda_str='ev : ev.y[0] >= 100',
                        )
                    )
                ),
                dict(
                    factory='NotFactory',
                    components=(
                        dict(
                            factory='AnyFactory',
                            components=(
                                dict(
                                    factory='LambdaStrFactory',
                                    components=(),
                                    lambda_str='ev : ev.z[0] == 0'
                                ),
                                dict(
                                    factory='LambdaStrFactory',
                                    components=(),
                                    lambda_str='ev : ev.w[0] >= 300',
                                ),
                            ),
                        ),
                    ),
                )
            )
        ),
        Any(
            name='Any',
            selections=[
                LambdaStr(
                    name='ev : ev.x[0] == 0',
                    lambda_str='ev : ev.x[0] == 0'
                ),
                All(
                    name='All',
                    selections=[
                        LambdaStr(
                            name='ev : ev.x[0] >= 1',
                            lambda_str='ev : ev.x[0] >= 1'),
                        LambdaStr(
                            name='ev : ev.y[0] >= 100',
                            lambda_str='ev : ev.y[0] >= 100')
                    ]
                ),
                Not(
                    name='Not',
                    selection=Any(
                        name='Any',
                        selections=[
                            LambdaStr(
                                name='ev : ev.z[0] == 0',
                                lambda_str='ev : ev.z[0] == 0'
                            ),
                            LambdaStr(
                                name='ev : ev.w[0] >= 300',
                                lambda_str='ev : ev.w[0] >= 300'
                            )
                        ]
                    )
                )
            ]
        ),
        id='example',
        ## marks=pytest.mark.skip(reason='not fully expanded')
    ),
]

@pytest.mark.parametrize('path_cfg, expected, _', params)
def test_expand_path_cfg(path_cfg, expected, _):
    actual = expand_path_cfg(path_cfg=path_cfg)
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual)
    assert expected == actual

@pytest.mark.parametrize('path_cfg, _, expected', params)
def test_factory(path_cfg, _, expected):

    kargs = dict(
        AllClass=All, AnyClass=Any, NotClass=Not,
        LambdaStrClass=LambdaStr,
        n=5242,
    )

    obj = FactoryDispatcher(path_cfg=path_cfg, **kargs)
    assert repr(expected) == repr(obj)
    assert str(expected) == str(obj)

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
