import unittest
import collections

from alphatwirl.loop import CollectorDelegate

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret = None):
        self.ret = ret

    def collect(self, dataset_readers_list):
        self.args = dataset_readers_list
        return self.ret

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
MockArgs = collections.namedtuple('MockArgs', 'name')

##__________________________________________________________________||
class TestCollectorDelegate(unittest.TestCase):

    def setUp(self):
        """
        1:delegate - 2:collector

        """
        self.result = MockResult('result')
        self.collector = MockCollector(ret = self.result)
        self.obj = CollectorDelegate(self.collector)

    def test_repr(self):
        repr(self.obj)

    def test_collect(self):

        args = MockArgs('args')
        self.assertIs(self.result, self.obj.collect(args))
        self.assertIs(args, self.collector.args)

##__________________________________________________________________||

