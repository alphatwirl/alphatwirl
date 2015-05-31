#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import CombineIntoList, WriteListToFile
from AlphaTwirl.HeppyResult import HeppyResult, EventBuilder, ComponentReaderComposite, ComponentLoop
from AlphaTwirl.Counter import Counts, GenericKeyComposerFactory, CounterFactory
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.EventReader import Collector, EventReaderCollectorAssociator, MPEventLoopRunner, EventReaderBundle,EventReaderCollectorAssociatorComposite
from AlphaTwirl.ProgressBar import BProgressMonitor, ProgressBar
from AlphaTwirl.Concurrently import CommunicationChannel

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/201525_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'

outPath1 = os.path.join(args.outdir, 'tbl_met.txt')
binning1 = RoundLog(0.1, 0)
keyComposer1 = GenericKeyComposerFactory(('met_pt', ), (binning1, ))
counterFactory1 = CounterFactory(Counts, keyComposer1, (binning1, ))
resultsCombinationMethod1 = CombineIntoList(('met', ))
deliveryMethod1 = WriteListToFile(outPath1)
collector1 = Collector(resultsCombinationMethod1, deliveryMethod1)
readerCollectorAssociator1 = EventReaderCollectorAssociator(counterFactory1, collector1)

outPath2 = os.path.join(args.outdir, 'tbl_jetpt.txt')
binning2 = RoundLog(0.1, 0)
keyComposer2 = GenericKeyComposerFactory(('jet_pt', ), (binning2, ), (0, ))
counterFactory2 = CounterFactory(Counts, keyComposer2, (binning2, ))
resultsCombinationMethod2 = CombineIntoList(('jet_pt', ))
deliveryMethod2 = WriteListToFile(outPath2)
collector2 = Collector(resultsCombinationMethod2, deliveryMethod2)
readerCollectorAssociator2 = EventReaderCollectorAssociator(counterFactory2, collector2)

outPath3 = os.path.join(args.outdir, 'tbl_njets_nbjets.txt')
binning31 = Echo()
binning32 = Echo()
keyComposer3 = GenericKeyComposerFactory(('nJet40', 'nBJet40'), (binning31, binning32))
counterFactory3 = CounterFactory(Counts, keyComposer3, (binning31, binning32))
resultsCombinationMethod3 = CombineIntoList(('njets', 'nbjets'))
deliveryMethod3 = WriteListToFile(outPath3)
collector3 = Collector(resultsCombinationMethod3, deliveryMethod3)
readerCollectorAssociator3 = EventReaderCollectorAssociator(counterFactory3, collector3)

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

progressBar = ProgressBar()
progressMonitor = BProgressMonitor(progressBar)
progressMonitor.begin()
communicationChannel = CommunicationChannel(8, progressMonitor)
communicationChannel.begin()
eventLoopRunner = MPEventLoopRunner(communicationChannel)

eventReaderCollectorAssociatorComposite = EventReaderCollectorAssociatorComposite(progressMonitor.createReporter())
eventReaderCollectorAssociatorComposite.add(readerCollectorAssociator1)
eventReaderCollectorAssociatorComposite.add(readerCollectorAssociator2)
eventReaderCollectorAssociatorComposite.add(readerCollectorAssociator3)
readerBundle = EventReaderBundle(eventBuilder, eventLoopRunner, eventReaderCollectorAssociatorComposite)

componentReaderComposite = ComponentReaderComposite()
componentReaderComposite.add(readerBundle)
componentLoop = ComponentLoop(componentReaderComposite)

heppyResult = HeppyResult(args.heppydir)

componentLoop(heppyResult.components())
communicationChannel.end()
progressMonitor.end()

##__________________________________________________________________||
