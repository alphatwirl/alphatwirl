# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReporter, ProgressReport

##__________________________________________________________________||
class MockQueue(object):
    def __init__(self): self.queue = [ ]
    def put(self, report): self.queue.append(report)
    def get(self): return self.queue.pop(0)
    def empty(self): return len(self.queue) == 0

##__________________________________________________________________||
def test_repr():
    queue = MockQueue()
    obj = ProgressReporter(queue)
    repr(obj)

def test_report(monkeypatch):
    queue = MockQueue()
    reporter = ProgressReporter(queue)

    mocktime = mock.MagicMock(return_value = 1000.0)
    monkeypatch.setattr(reporter, '_time', mocktime)

    reporter._readTime()
    assert 1000.0 == reporter.lastTime

    mocktime.return_value = 1000.2
    reporter._report(ProgressReport(name = "dataset1", done = 124, total = 1552))

    report = queue.get()
    assert "dataset1" == report.name
    assert 124 == report.done
    assert 1552 == report.total

    assert 1000.2 == reporter.lastTime

def test_needToReport(monkeypatch):
    queue = MockQueue()
    reporter = ProgressReporter(queue)

    interval = reporter.interval
    assert 0.1 == interval

    mocktime = mock.MagicMock(return_value = 1000.0)
    monkeypatch.setattr(reporter, '_time', mocktime)

    reporter._readTime()
    assert 1000.0 == reporter.lastTime

    # before the interval passes
    mocktime.return_value += 0.1*interval
    report = ProgressReport(name = "dataset1", done = 124, total = 1552)
    assert not reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

    # the last report before the interval passes
    report = ProgressReport(name = "dataset1", done = 1552, total = 1552)
    assert reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

    # after the interval passes
    mocktime.return_value += 1.2*interval
    report = ProgressReport(name = "dataset2", done = 1022, total = 4000)
    assert reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

##__________________________________________________________________||
