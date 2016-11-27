from AlphaTwirl.Summary import Count, KeyValueComposer, NextKeyComposer, Reader
from AlphaTwirl.Binning import Echo
from AlphaTwirl.Loop import Associator
from AlphaTwirl.Loop import ReaderComposite
from AlphaTwirl.Loop import Collector, CollectorComposite, CollectorDelegate
import unittest

##__________________________________________________________________||
class MockProgressReporter(object): pass

##__________________________________________________________________||
class MockResultsCombinationMethod(object):
    def combine(self, pairs) :pass

##__________________________________________________________________||
class TesEventReader_build_01(unittest.TestCase):

    def test_two(self):
        """
        1:composite
            |- 3:composite
            |  |- 4:counter
            |  |- 5:counter
            |
            |- 7:counter
            |- 8:counter
        """

        progressReporter1 = MockProgressReporter()

        keyComposer4 = KeyValueComposer(('var4', ), (Echo(), ))
        counts4 = Count()
        reader4 = Reader(keyComposer4, counts4)
        collector4 = Collector(MockResultsCombinationMethod())

        keyComposer5 = KeyValueComposer(('var5', ), (Echo(), ))
        counts5 = Count()
        reader5 = Reader(keyComposer5, counts5)
        collector5 = Collector(MockResultsCombinationMethod())

        keyComposer7 = KeyValueComposer(('var7', ), (Echo(), ))
        counts7 = Count()
        reader7 = Reader(keyComposer7, counts7)
        collector7 = Collector(MockResultsCombinationMethod())

        keyComposer8 = KeyValueComposer(('var8', ), (Echo(), ))
        counts8 = Count()
        reader8 = Reader(keyComposer8, counts8)
        collector8 = Collector(MockResultsCombinationMethod())

        reader3 = ReaderComposite()
        reader3.add(reader4)
        reader3.add(reader5)

        collector3 = CollectorComposite(progressReporter1)
        collector3.add(collector4)
        collector3.add(collector5)

        reader1 = ReaderComposite()
        reader1.add(reader3)
        reader1.add(reader7)
        reader1.add(reader8)

        collector1 = CollectorComposite(progressReporter1)
        collector1.add(collector3)
        collector1.add(collector7)
        collector1.add(collector8)

        associator1 = Associator(reader1, collector1)

        reader1_ds1 = associator1.make('ds1')
        reader1_ds2 = associator1.make('ds2')

        reader3_ds1 = reader1_ds1.readers[0]
        reader4_ds1 = reader3_ds1.readers[0]
        reader5_ds1 = reader3_ds1.readers[1]
        reader7_ds1 = reader1_ds1.readers[1]
        reader8_ds1 = reader1_ds1.readers[2]

        self.assertIsInstance(reader1_ds1, ReaderComposite)
        self.assertIsInstance(reader3_ds1, ReaderComposite)
        self.assertIsInstance(reader4_ds1, Reader)
        self.assertIsInstance(reader5_ds1, Reader)
        self.assertIsInstance(reader7_ds1, Reader)
        self.assertIsInstance(reader8_ds1, Reader)

        self.assertIsNot(reader1, reader1_ds1)
        self.assertIsNot(reader3, reader3_ds1)
        self.assertIsNot(reader4, reader4_ds1)
        self.assertIsNot(reader5, reader5_ds1)
        self.assertIsNot(reader7, reader7_ds1)
        self.assertIsNot(reader8, reader8_ds1)

        reader3_ds2 = reader1_ds2.readers[0]
        reader4_ds2 = reader3_ds2.readers[0]
        reader5_ds2 = reader3_ds2.readers[1]
        reader7_ds2 = reader1_ds2.readers[1]
        reader8_ds2 = reader1_ds2.readers[2]

        self.assertIsInstance(reader1_ds2, ReaderComposite)
        self.assertIsInstance(reader3_ds2, ReaderComposite)
        self.assertIsInstance(reader4_ds2, Reader)
        self.assertIsInstance(reader5_ds2, Reader)
        self.assertIsInstance(reader7_ds2, Reader)
        self.assertIsInstance(reader8_ds2, Reader)

        self.assertIsNot(reader1, reader1_ds2)
        self.assertIsNot(reader3, reader3_ds2)
        self.assertIsNot(reader4, reader4_ds2)
        self.assertIsNot(reader5, reader5_ds2)
        self.assertIsNot(reader7, reader7_ds2)
        self.assertIsNot(reader8, reader8_ds2)

        self.assertIs(2, len(collector4._datasetReaderPairs))
        self.assertIs(2, len(collector5._datasetReaderPairs))
        self.assertIs(2, len(collector7._datasetReaderPairs))
        self.assertIs(2, len(collector8._datasetReaderPairs))

        self.assertIs('ds1', collector4._datasetReaderPairs[0][0])
        self.assertIs('ds1', collector5._datasetReaderPairs[0][0])
        self.assertIs('ds1', collector7._datasetReaderPairs[0][0])
        self.assertIs('ds1', collector8._datasetReaderPairs[0][0])
        self.assertIs(reader4_ds1, collector4._datasetReaderPairs[0][1])
        self.assertIs(reader5_ds1, collector5._datasetReaderPairs[0][1])
        self.assertIs(reader7_ds1, collector7._datasetReaderPairs[0][1])
        self.assertIs(reader8_ds1, collector8._datasetReaderPairs[0][1])

        self.assertIs('ds2', collector4._datasetReaderPairs[1][0])
        self.assertIs('ds2', collector5._datasetReaderPairs[1][0])
        self.assertIs('ds2', collector7._datasetReaderPairs[1][0])
        self.assertIs('ds2', collector8._datasetReaderPairs[1][0])
        self.assertIs(reader4_ds2, collector4._datasetReaderPairs[1][1])
        self.assertIs(reader5_ds2, collector5._datasetReaderPairs[1][1])
        self.assertIs(reader7_ds2, collector7._datasetReaderPairs[1][1])
        self.assertIs(reader8_ds2, collector8._datasetReaderPairs[1][1])

##__________________________________________________________________||
