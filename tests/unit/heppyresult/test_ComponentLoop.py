# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.heppyresult import ComponentLoop

##__________________________________________________________________||
@pytest.fixture()
def reader():
    return mock.Mock()

@pytest.fixture()
def components():
    component1 = mock.Mock()
    component2 = mock.Mock()
    return [component1, component2]

@pytest.fixture()
def heppyresult(components):
    ret = mock.Mock()
    ret.components.return_value = components
    return ret

@pytest.fixture()
def obj(heppyresult, reader):
    return ComponentLoop(heppyresult, reader)

def test_repr(obj):
    repr(obj)

def test_call(obj, reader, components, heppyresult):
    result = obj()
    assert [mock.call()] == reader.begin.call_args_list
    assert [mock.call()] == heppyresult.components.call_args_list
    assert [mock.call(c) for c in components] == reader.read.call_args_list
    assert reader.end() is result

def test_deprecated(caplog, heppyresult, reader):
    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        ComponentLoop(heppyresult, reader)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'ComponentLoop' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

##__________________________________________________________________||
