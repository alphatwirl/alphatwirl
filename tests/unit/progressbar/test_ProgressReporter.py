# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.progressbar import ProgressReporter

##__________________________________________________________________||
@pytest.fixture()
def queue():
    return mock.MagicMock()

@pytest.fixture()
def reporter(queue):
    return ProgressReporter(queue)

##__________________________________________________________________||
def test_repr(reporter):
    repr(reporter)

def test_report(reporter, queue, monkeypatch):

    mocktime = mock.MagicMock(return_value = 1000.0)
    monkeypatch.setattr(reporter, '_time', mocktime)

    reporter._readTime()
    assert 1000.0 == reporter.lastTime

    report = mock.MagicMock(name = "dataset1", done = 124, total = 1552)
    mocktime.return_value = 1000.2
    reporter._report(report)

    assert [mock.call(report)] == queue.put.call_args_list

    assert 1000.2 == reporter.lastTime

def test_needToReport(reporter, queue, monkeypatch):

    interval = reporter.interval
    assert 0.1 == interval

    mocktime = mock.MagicMock(return_value = 1000.0)
    monkeypatch.setattr(reporter, '_time', mocktime)

    reporter._readTime()
    assert 1000.0 == reporter.lastTime

    # before the interval passes
    mocktime.return_value += 0.1*interval
    report = mock.MagicMock(name = "dataset1", done = 124, total = 1552)
    assert not reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

    # the last report before the interval passes
    report = mock.MagicMock(name = "dataset1", done = 1552, total = 1552)
    assert reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

    # after the interval passes
    mocktime.return_value += 1.2*interval
    report = mock.MagicMock(name = "dataset2", done = 1022, total = 4000)
    assert reporter._needToReport(report)
    assert 1000.0 == reporter.lastTime

##__________________________________________________________________||
