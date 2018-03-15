# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.selection.factories.expand import expand_path_cfg

from alphatwirl.selection.factories.factory import FactoryDispatcher
from alphatwirl.selection.modules.LambdaStr import LambdaStr
from alphatwirl.selection.modules import All, Any, Not

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
# path_cfg, expanded, obj
params = [
    pytest.param(
        'alias1',
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias1'
        ),
        LambdaStr(
            name='alias1',
            lambda_str='ev : ev.var1[0] >= 10'
        ),
        id='alias1'
    ),
    pytest.param(
        ('alias1', dict(name='name1')),
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var1[0] >= 10',
            name='name1'
        ),
        LambdaStr(name='name1', lambda_str='ev : ev.var1[0] >= 10'),
        id='alias1:with-name'
    ),
    pytest.param(
        'alias2',
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var2[0] >= 20',
            name='name2' #  name has priority over alias
        ),
        LambdaStr(name='name2', lambda_str='ev : ev.var2[0] >= 20'),
        id='alias2:name-priority-over-alias'
    ),
    pytest.param(
        ('alias2', dict(name='new_name2')),
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var2[0] >= 20',
            name='new_name2' # name can be overridden
        ),
        LambdaStr(name='new_name2', lambda_str='ev : ev.var2[0] >= 20'),
        id='alias2:name-overridden'
    ),
    pytest.param(
        'alias3',
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias3' # the outermost alias has priority
        ),
        LambdaStr(name='alias3', lambda_str='ev : ev.var1[0] >= 10'),
        id='alias3:alias-of-alias'
    ),
    pytest.param(
        'alias4',
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var1[0] >= 10',
            name='alias4' # the outermost alias has priority
        ),
        LambdaStr(name='alias4', lambda_str='ev : ev.var1[0] >= 10'),
        id='alias4:alias-of-alias-of-alias'
    ),
    pytest.param(
        ('alias5', dict(n=30)),
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : ev.var4[0] == {n}', # not formatted
            n=30,
            name='alias5'
        ),
        LambdaStr(name='alias5', lambda_str='ev : ev.var4[0] == 30'),
        id='alias5:not-formatted'
    ),
    pytest.param(
        'alias6',
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : {low} <= ev.var5[0] < {high}',
            low=11,
            high=20,
            name='alias6',
        ),
        LambdaStr(name='alias6', lambda_str='ev : 11 <= ev.var5[0] < 20'),
        id='alias6:not-formatted-with-default-values'
    ),
    pytest.param(
        ('alias6', dict(high=30)),
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : {low} <= ev.var5[0] < {high}',
            low=11,
            high=30,
            name='alias6'
        ),
        LambdaStr(name='alias6', lambda_str='ev : 11 <= ev.var5[0] < 30'),
        id='alias6:not-formatted-with-default-values-overridden'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, expected, _', params)
def test_alias(alias_dict, path_cfg, expected, _):
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual, alias_dict=alias_dict)
    assert expected == actual


@pytest.mark.parametrize('path_cfg, expected, _', params)
def test_nested(alias_dict, path_cfg, expected, _):
    path_cfg = dict(All=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AllFactory', components=(expected, ))
    assert expected == actual

    path_cfg = dict(All=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AllFactory', components=(expected, ))
    assert expected == actual

    path_cfg = dict(Not=path_cfg)
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='NotFactory', components=(expected, ))
    assert expected == actual

    path_cfg = dict(Any=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AnyFactory', components=(expected, ))
    assert expected == actual

    path_cfg = dict(Any=(path_cfg, ))
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='AnyFactory', components=(expected, ))
    assert expected == actual

    path_cfg = dict(Not=path_cfg)
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    expected = dict(factory='NotFactory', components=(expected, ))
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual, alias_dict=alias_dict)
    assert expected == actual

##__________________________________________________________________||
@pytest.mark.parametrize('path_cfg, _, expected', params)
def test_factory(alias_dict, path_cfg, _, expected):

    kargs = dict(
        AllClass=All, AnyClass=Any, NotClass=Not,
        LambdaStrClass=LambdaStr, aliasDict=alias_dict,
    )

    obj = FactoryDispatcher(path_cfg=path_cfg, **kargs)
    assert repr(expected) == repr(obj)
    assert str(expected) == str(obj)

@pytest.mark.parametrize('path_cfg, _, expected', params)
def test_factory_nested(alias_dict, path_cfg, _, expected):

    kargs = dict(
        AllClass=All, AnyClass=Any, NotClass=Not,
        LambdaStrClass=LambdaStr, aliasDict=alias_dict,
    )

    path_cfg = dict(All=(path_cfg, ))
    expected = All(name='All', selections=[expected])

    path_cfg = dict(All=(path_cfg, ))
    expected = All(name='All', selections=[expected])

    path_cfg = dict(Not=path_cfg)
    expected = Not(name='Not', selection=expected)

    path_cfg = dict(Any=(path_cfg, ))
    expected = Any(name='Any', selections=[expected])

    path_cfg = dict(Any=(path_cfg, ))
    expected = Any(name='Any', selections=[expected])

    path_cfg = dict(Not=path_cfg)
    expected = Not(name='Not', selection=expected)

    obj = FactoryDispatcher(path_cfg=path_cfg, **kargs)
    assert repr(expected) == repr(obj)
    assert str(expected) == str(obj)

##__________________________________________________________________||
