from AlphaTwirl.Loop import CollectorComposite, ReaderComposite
import unittest

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self):
        self._datasetReaderPairs = [ ]
        self._collected = False

    def addReader(self, datasetName, reader):
        self._datasetReaderPairs.append((datasetName, reader))

    def collect(self):
        self._collected = True

##__________________________________________________________________||
class MockReader(object):
    pass

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
        collector3 = MockCollector()
        collector4 = MockCollector()
        collector5 = MockCollector()

        collector1.add(collector2)
        collector2.add(collector3)
        collector2.add(collector4)
        collector1.add(collector5)

        reader1 = ReaderComposite()
        reader2 = ReaderComposite()
        reader3 = MockReader()
        reader4 = MockReader()
        reader5 = MockReader()

        reader1.add(reader2)
        reader2.add(reader3)
        reader2.add(reader4)
        reader1.add(reader5)

        collector1.addReader('ds1', reader1)

        self.assertEqual('ds1', collector3._datasetReaderPairs[0][0])
        self.assertEqual('ds1', collector4._datasetReaderPairs[0][0])
        self.assertEqual('ds1', collector5._datasetReaderPairs[0][0])

        self.assertIs(reader3, collector3._datasetReaderPairs[0][1])
        self.assertIs(reader4, collector4._datasetReaderPairs[0][1])
        self.assertIs(reader5, collector5._datasetReaderPairs[0][1])

        self.assertFalse(collector3._collected)
        self.assertFalse(collector4._collected)
        self.assertFalse(collector5._collected)

        collector1.collect()

        self.assertTrue(collector3._collected)
        self.assertTrue(collector4._collected)
        self.assertTrue(collector5._collected)

##__________________________________________________________________||

