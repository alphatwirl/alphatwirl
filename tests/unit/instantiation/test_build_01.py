from AlphaTwirl.Counter import Counts, GenericKeyComposerFactory, CounterFactory, Counter
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.EventReader import Collector, EventReaderCollectorAssociator, EventReaderCollectorAssociatorComposite
import unittest

##__________________________________________________________________||
class MockProgressReporter(object): pass

##__________________________________________________________________||
class MockResultsCombinationMethod(object):
    def combine(self, pairs) :pass

##____________________________________________________________________________||
class TestBuild01(unittest.TestCase):

    def test_one(self):

        # Initialize
        binning1 = RoundLog(0.1, 1)
        keyComposer1 = GenericKeyComposerFactory(('met_pt', ), (binning1, ))
        counterFactory1 = CounterFactory(Counts, keyComposer1, (binning1, ))
        collector1 = Collector(MockResultsCombinationMethod())
        readerCollectorAssociator1 = EventReaderCollectorAssociator(counterFactory1, collector1)

        binning31 = Echo()
        binning32 = Echo()
        keyComposer3 = GenericKeyComposerFactory(('nJet40', 'nBJet40'), (binning31, binning32))
        counterFactory3 = CounterFactory(Counts, keyComposer3, (binning31, binning32))
        collector3 = Collector(MockResultsCombinationMethod())
        readerCollectorAssociator3 = EventReaderCollectorAssociator(counterFactory3, collector3)

        progressReporter1 = MockProgressReporter()
        eventReaderCollectorAssociatorComposite = EventReaderCollectorAssociatorComposite(progressReporter1)
        eventReaderCollectorAssociatorComposite.add(readerCollectorAssociator1)
        eventReaderCollectorAssociatorComposite.add(readerCollectorAssociator3)

        collectorComposite = eventReaderCollectorAssociatorComposite.collector

        # Loop over data sets
        readerComposite_TTJets = eventReaderCollectorAssociatorComposite.make('TTJets')
        self.assertEqual(2, len(readerComposite_TTJets.readers))
        self.assertIsInstance(readerComposite_TTJets.readers[0], Counter)
        self.assertEqual(('met_pt', ), readerComposite_TTJets.readers[0].keyComposer.branchNames)
        self.assertIsInstance(readerComposite_TTJets.readers[1], Counter)
        self.assertEqual(('nJet40', 'nBJet40'), readerComposite_TTJets.readers[1].keyComposer.branchNames)

        readerComposite_DYJetsToLL = eventReaderCollectorAssociatorComposite.make('DYJetsToLL')
        self.assertEqual(2, len(readerComposite_DYJetsToLL.readers))
        self.assertIsInstance(readerComposite_DYJetsToLL.readers[0], Counter)
        self.assertEqual(('met_pt', ), readerComposite_DYJetsToLL.readers[0].keyComposer.branchNames)
        self.assertIsInstance(readerComposite_DYJetsToLL.readers[1], Counter)
        self.assertEqual(('nJet40', 'nBJet40'), readerComposite_DYJetsToLL.readers[1].keyComposer.branchNames)


        # Assert that the collectors are correctly placed
        self.assertEqual(2, len(collectorComposite.components))
        self.assertIs(collector1, collectorComposite.components[0])
        self.assertIs(collector3, collectorComposite.components[1])

        self.assertEqual(2, len(collector1._datasetReaderPairs))
        self.assertEqual('TTJets', collector1._datasetReaderPairs[0][0])
        self.assertIs(readerComposite_TTJets.readers[0], collector1._datasetReaderPairs[0][1])
        self.assertEqual('DYJetsToLL', collector1._datasetReaderPairs[1][0])
        self.assertIs(readerComposite_DYJetsToLL.readers[0], collector1._datasetReaderPairs[1][1])

        self.assertEqual(2, len(collector3._datasetReaderPairs))
        self.assertEqual('TTJets', collector3._datasetReaderPairs[0][0])
        self.assertIs(readerComposite_TTJets.readers[1], collector3._datasetReaderPairs[0][1])
        self.assertEqual('DYJetsToLL', collector3._datasetReaderPairs[1][0])
        self.assertIs(readerComposite_DYJetsToLL.readers[1], collector3._datasetReaderPairs[1][1])

        self.assertIs(progressReporter1, collectorComposite.progressReporter)

##____________________________________________________________________________||
