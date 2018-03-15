# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.selection.factories.expand import expand_path_cfg

##__________________________________________________________________||
@pytest.fixture()
def alias_dict():
    return {
        'var_cut': ('ev : {low} <= ev.var[0] < {high}', dict(low=10, high=200)),
    }

##__________________________________________________________________||
params = [
    pytest.param(
        ('var_cut', dict(name='var_cut25', low=25)),
        dict(
            factory='LambdaStrFactory',
            components=(),
            lambda_str='ev : {low} <= ev.var[0] < {high}',
            name='var_cut25',
            low=25, high=200,
        ),
        id='example1'
    ),
]

@pytest.mark.parametrize('path_cfg, expected', params)
def test_alias(alias_dict, path_cfg, expected):
    actual = expand_path_cfg(path_cfg=path_cfg, alias_dict=alias_dict)
    assert expected == actual

    # give expanded one
    actual = expand_path_cfg(path_cfg=actual, alias_dict=alias_dict)
    assert expected == actual


##__________________________________________________________________||
