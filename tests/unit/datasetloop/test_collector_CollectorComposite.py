# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

try:
    import unittest.mock as mock
    from unittest.mock import call, sentinel
except ImportError:
    import mock
    from mock import call, sentinel

from alphatwirl.datasetloop import CollectorComposite
from atpbar import atpbar

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return CollectorComposite()

def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
@pytest.fixture()
def mock_atpbar(monkeypatch):
    ret = mock.Mock(wraps=atpbar)
    module = sys.modules['alphatwirl.datasetloop.collector']
    monkeypatch.setattr(module, 'atpbar', ret)
    return ret

##__________________________________________________________________||
class MockCollector:
   def __init__(self, name):
      self.name = name
   def __call__(self, dataset_reader_list):
      return {self.name: dataset_reader_list}

##__________________________________________________________________||
def test_call(obj, mock_atpbar):

   collector1 = MockCollector(name='collector1')
   collector2 = MockCollector(name='collector2')
   collector3 = MockCollector(name='collector3')

   collectors = [collector1, collector2, collector3]
   for collector in collectors:
      obj.add(collector)

   dataset_result_list = [
      ['QCD',    [sentinel.result11, sentinel.result21, sentinel.result31]],
      ['TTJets', [sentinel.result12, sentinel.result22, sentinel.result32]],
      ['WJets',  [sentinel.result13, sentinel.result23, sentinel.result33]],
   ]

   expected = [
      dict(collector1=(('QCD', sentinel.result11), ('TTJets', sentinel.result12), ('WJets', sentinel.result13))),
      dict(collector2=(('QCD', sentinel.result21), ('TTJets', sentinel.result22), ('WJets', sentinel.result23))),
      dict(collector3=(('QCD', sentinel.result31), ('TTJets', sentinel.result32), ('WJets', sentinel.result33)))
   ]

   assert expected == obj(dataset_result_list)

   assert [call(collectors, name='collecting results')] == mock_atpbar.call_args_list

##__________________________________________________________________||
