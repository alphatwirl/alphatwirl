# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.heppyresult import EventBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def mockBaseEventBuilder(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.heppyresult.EventBuilder']
    monkeypatch.setattr(module, 'BEventBuilder', ret)
    return ret

##__________________________________________________________________||
def test_repr(mockBaseEventBuilder):
    config = mock.Mock()
    obj = EventBuilder(config)
    repr(obj)

def test_build(mockBaseEventBuilder):
    config = mock.Mock()
    obj = EventBuilder(config)
    events = obj()
    assert mockBaseEventBuilder()() is events

##__________________________________________________________________||
