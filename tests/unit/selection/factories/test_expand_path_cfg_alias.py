# Tai Sakuma <tai.sakuma@gmail.com>
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
params = [
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
]

@pytest.mark.parametrize('path_cfg, expected', params)
def test_alias(alias_dict, path_cfg, expected):
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual, alias_dict=alias_dict)
    assert expected == actual


@pytest.mark.parametrize('path_cfg, expected', params)
def test_nested(alias_dict, path_cfg, expected):
    path_cfg = dict(All=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AllFactory', path_cfg_list=(expected, ))
    assert expected == actual

    path_cfg = dict(All=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AllFactory', path_cfg_list=(expected, ))
    assert expected == actual

    path_cfg = dict(Not=path_cfg)
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='NotFactory', path_cfg=expected)
    assert expected == actual

    path_cfg = dict(Any=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AnyFactory', path_cfg_list=(expected, ))
    assert expected == actual

    path_cfg = dict(Any=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AnyFactory', path_cfg_list=(expected, ))
    assert expected == actual

    path_cfg = dict(Not=path_cfg)
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='NotFactory', path_cfg=expected)
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual, alias_dict=alias_dict)
    assert expected == actual

##__________________________________________________________________||
