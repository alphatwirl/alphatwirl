import unittest
import collections

from alphatwirl.loop import CollectorDelegate

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret = None):
        self.ret = ret

    def collect(self, dataset_reader_pairs):
        self.pairs = dataset_reader_pairs
        return self.ret

##__________________________________________________________________||
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
MockPairs = collections.namedtuple('MockPairs', 'name')

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

        pairs = MockPairs('pairs')
        self.assertIs(self.result, self.obj.collect(pairs))
        self.assertIs(pairs, self.collector.pairs)

##__________________________________________________________________||

