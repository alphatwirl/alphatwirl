import unittest

import copy
import collections


from alphatwirl.loop import CollectorComposite, ReaderComposite

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret = None):
        self.collected = False
        self.ret = ret

        self.pairs = [ ]

    def collect(self, dataset_reader_pairs):
        self.pairs = dataset_reader_pairs
        self.collected = True
        return self.ret

##__________________________________________________________________||
MockReader = collections.namedtuple('MockReader', 'name')

##__________________________________________________________________||
class TestCollectorComposite(unittest.TestCase):

    def test_repr(self):
        obj = CollectorComposite()
        repr(obj)

    def test_collect(self):
        """
        1:composite
            |- 2:composite
            |        |- 3:leaf
            |        |- 4:leaf
            |
            |- 5:leaf
        """
        collector1 = CollectorComposite()
        collector2 = CollectorComposite()
        collector3 = MockCollector('result3')
        collector4 = MockCollector('result4')
        collector5 = MockCollector('result5')

        collector1.add(collector2)
        collector2.add(collector3)
        collector2.add(collector4)
        collector1.add(collector5)

        reader1 = ReaderComposite()
        reader2 = ReaderComposite()
        reader3 = MockReader('name3')
        reader4 = MockReader('name4')
        reader5 = MockReader('name5')

        reader1.add(reader2)
        reader2.add(reader3)
        reader2.add(reader4)
        reader1.add(reader5)

        self.assertFalse(collector3.collected)
        self.assertFalse(collector4.collected)
        self.assertFalse(collector5.collected)

        self.assertEqual([['result3', 'result4'], 'result5'],
                         collector1.collect([['ds1', reader1], ['ds2', copy.copy(reader1)]]))

        self.assertEqual([('ds1', reader3), ('ds2', reader3)], collector3.pairs)
        self.assertEqual([('ds1', reader4), ('ds2', reader4)], collector4.pairs)
        self.assertEqual([('ds1', reader5), ('ds2', reader5)], collector5.pairs)

        self.assertTrue(collector3.collected)
        self.assertTrue(collector4.collected)
        self.assertTrue(collector5.collected)

##__________________________________________________________________||

