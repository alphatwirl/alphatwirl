# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.factories.factory import LambdaStrFactory

##__________________________________________________________________||
@pytest.fixture()
def MockLambdaStr():
    return mock.Mock()

@pytest.mark.parametrize('kwargs, expected', [
    pytest.param(
        dict(
            lambda_str='ev : ev.var1[0] >= 10',
            name='var1',
        ),
        dict(
            lambda_str='ev : ev.var1[0] >= 10',
            name='var1'
        ),
        id='simple',
    ),
    pytest.param(
        dict(
            lambda_str='ev : ev.var1[0] >= 10',
        ),
        dict(
            lambda_str='ev : ev.var1[0] >= 10',
            name=None,
        ),
        id='no-name',
    ),
    pytest.param(
        dict(
            lambda_str = 'ev : {low} <= ev.var1[0] = {high}',
            name='var1', low=100, high=200,
        ),
        dict(
            lambda_str = 'ev : 100 <= ev.var1[0] = 200',
            name='var1'
        ),
        id='format',
    ),
])
def test_call(kwargs, expected, MockLambdaStr):
    actual = LambdaStrFactory(LambdaStrClass=MockLambdaStr, **kwargs)
    assert [mock.call(**expected)] == MockLambdaStr.call_args_list
    assert actual == MockLambdaStr()

##__________________________________________________________________||
