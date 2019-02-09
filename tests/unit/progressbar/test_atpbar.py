# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import pytest

import alphatwirl
from alphatwirl.progressbar import atpbar

try:
    import unittest.mock as mock
except ImportError:
    import mock

##__________________________________________________________________||
@pytest.fixture()
def mock_report_progress(monkeypatch):
    ret = mock.Mock()
    monkeypatch.setattr(alphatwirl.progressbar, 'report_progress', ret)
    return ret

##__________________________________________________________________||
def test_iteration(mock_report_progress):

    iterable = range(4)
    returned = [ ]

    for e in atpbar(iterable):
        returned.append(e)

    assert [0, 1, 2, 3] == returned
    assert 4 == len(mock_report_progress.call_args_list)

    for i, c in enumerate(mock_report_progress.call_args_list):
        args, kwargs = c
        report = args[0]
        assert i + 1 == report.done
        assert 4 == report.total

##__________________________________________________________________||
