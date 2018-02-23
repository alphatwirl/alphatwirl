# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import EventLoop
from alphatwirl import progressbar

##__________________________________________________________________||
@pytest.fixture()
def events():
    event1 = mock.Mock(name='event1')
    event2 = mock.Mock(name='event2')
    event3 = mock.Mock(name='event3')
    return [event1, event2, event3]

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

##__________________________________________________________________||
def test_name(build_events, reader):
    obj = EventLoop(build_events, reader)
    assert 'EventLoop' == obj.name

    obj = EventLoop(build_events, reader, name='TTJets')
    assert 'TTJets' == obj.name

def test_repr(obj):
    repr(obj)

def test_call(obj, events, reader):

    assert reader == obj()

    assert [
        mock.call.begin(events),
        mock.call.event(events[0]),
        mock.call.event(events[1]),
        mock.call.event(events[2]),
        mock.call.end()] == reader.method_calls

##__________________________________________________________________||
@pytest.fixture()
def report_progress(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.progressbar']
    monkeypatch.setattr(module, 'report_progress', ret)
    return ret

@pytest.fixture()
def ProgressReport(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.loop.EventLoop']
    monkeypatch.setattr(module, 'ProgressReport', ret)
    return ret

def test_report_progress(obj, report_progress, ProgressReport):
    obj()
    expected = [
        mock.call(ProgressReport(taskid=obj.taskid, name='EventLoop', done=0, total=3)),
        mock.call(ProgressReport(taskid=obj.taskid, name='EventLoop', done=1, total=3)),
        mock.call(ProgressReport(taskid=obj.taskid, name='EventLoop', done=2, total=3)),
        mock.call(ProgressReport(taskid=obj.taskid, name='EventLoop', done=3, total=3))
    ]
    actual = report_progress.call_args_list
    assert expected[0] == actual[0]

##__________________________________________________________________||
