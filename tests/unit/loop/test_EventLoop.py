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
@pytest.fixture()
def report_progress(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.progressbar']
    monkeypatch.setattr(module, 'report_progress', ret)
    return ret

@pytest.fixture()
def ProgressReport(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.progressbar']
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
