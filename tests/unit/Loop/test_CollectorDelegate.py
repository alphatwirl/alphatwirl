from AlphaTwirl.Loop import CollectorDelegate
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
class MockReaderDelegate(object):
    def __init__(self, reader):
        self.reader = reader

##__________________________________________________________________||
class TestCollectorDelegate(unittest.TestCase):

    def test_collect(self):
        """
        1:delegate - 2:collector

        """
        collector2 = MockCollector()
        collector1 = CollectorDelegate(collector2)

        reader2 = MockReader()
        reader1 = MockReaderDelegate(reader2)

        collector1.addReader('ds1', reader1)

        self.assertEqual('ds1', collector2._datasetReaderPairs[0][0])
        self.assertIs(reader2, collector2._datasetReaderPairs[0][1])


        self.assertFalse(collector2._collected)
        collector1.collect()
        self.assertTrue(collector2._collected)

##__________________________________________________________________||

