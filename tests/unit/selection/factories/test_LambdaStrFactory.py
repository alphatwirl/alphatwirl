# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.factories.factory import LambdaStrFactory

##__________________________________________________________________||
def test_LambdaStrFactory():
    lambda_str = mock.Mock()
    MockClass = mock.Mock()
    components = ()
    name = mock.sentinel.name
    obj = LambdaStrFactory(lambda_str=lambda_str, LambdaStrClass=MockClass,
                           name=name, components=())
    assert [mock.call(lambda_str=lambda_str.format(), name=name)] == MockClass.call_args_list
    assert obj == MockClass()

##__________________________________________________________________||
