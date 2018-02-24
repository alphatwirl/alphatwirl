# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl import progressbar

##__________________________________________________________________||
@pytest.fixture()
def mocsys(monkeypatch):
    ret = mock.Mock()
    module = sys.modules['alphatwirl.progressbar.ProgressPrint']
    monkeypatch.setattr(module, 'sys', ret)
    return ret

@pytest.fixture()
def moctime(monkeypatch):
    ret = mock.MagicMock()
    module = sys.modules['alphatwirl.progressbar.ProgressPrint']
    monkeypatch.setattr(module, 'time', ret)
    return ret

@pytest.fixture()
def obj():
    return progressbar.ProgressPrint()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_report(obj, mocsys, moctime):
    report = progressbar.ProgressReport('task1', 0, 10)
    # obj.present(report)
    # print 
    # print mocsys.stdout.write.call_args_list
    # print mocsys.method_calls
    # print mocsys.mock_calls

##__________________________________________________________________||
