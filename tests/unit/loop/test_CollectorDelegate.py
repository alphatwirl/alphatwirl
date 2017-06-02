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

    def test_collect(self):
        """
        1:delegate - 2:collector

        """
        result = MockResult('result')
        collector2 = MockCollector(ret = result)
        collector1 = CollectorDelegate(collector2)

        pairs = MockPairs('pairs')
        self.assertIs(result, collector1.collect(pairs))
        self.assertIs(pairs, collector2.pairs)

##__________________________________________________________________||

