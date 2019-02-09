# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import EventLoop
from alphatwirl.progressbar import atpbar

##__________________________________________________________________||
@pytest.fixture(params=[0, 3])
def events(request):
    nevents = request.param
    ret = [mock.Mock(name='event{}'.format(i)) for i in range(nevents)]
    # e.g., [mock.Mock(name='event0'), mock.Mock(name='event1'), ...]
    return ret

@pytest.fixture()
def build_events(events):
    ret = mock.Mock()
    ret.return_value = events
    return ret

@pytest.fixture()
def reader():
    return mock.Mock()

@pytest.fixture()
def obj(build_events, reader):
    return EventLoop(build_events, reader)

@pytest.fixture()
def mock_atpbar(monkeypatch):
    ret = mock.Mock(wraps=atpbar)
    module = sys.modules['alphatwirl.loop.EventLoop']
    monkeypatch.setattr(module, 'atpbar', ret)
    return ret

##__________________________________________________________________||
def test_progressbar_label(build_events, reader):
    obj = EventLoop(build_events, reader)
    assert 'EventLoop' == obj.progressbar_label

    obj = EventLoop(build_events, reader, progressbar_label='TTJets')
    assert 'TTJets' == obj.progressbar_label

def test_repr(obj):
    repr(obj)

def test_call(obj, events, reader):

    assert reader == obj()

    expected = [ ]
    expected.append(mock.call.begin(events)) # begin will called even
                                             # if len(events) == 0
    expected.extend([mock.call.event(e) for e in events])
    expected.append(mock.call.end())
    assert expected == reader.method_calls

##__________________________________________________________________||
def test_atpbar(obj, mock_atpbar, events, reader):
    assert reader == obj()
    expected = [mock.call(events, name='EventLoop')]
    assert expected == mock_atpbar.call_args_list

##__________________________________________________________________||
