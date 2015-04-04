#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import EventBuilder, CombineIntoPandasDataFrame, WritePandasDataFrameToFile, HeppyResultReader
from AlphaTwirl.HeppyResult import HeppyResult
from AlphaTwirl.Counter import Counts, GenericKeyComposer, CounterBuilder
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.EventReader import Collector, EventReaderPackage, MPEventLoopRunner, EventReaderBundle
from AlphaTwirl.ProgressBar import MPProgressMonitor, ProgressBar

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
keyComposer1 = GenericKeyComposer(('met_pt', ), (binning1, ))
counterBuilder1 = CounterBuilder(Counts, ('met', ), keyComposer1)
resultsCombinationMethod1 = CombineIntoPandasDataFrame()
deliveryMethod1 = WritePandasDataFrameToFile(outPath1)
collector1 = Collector(resultsCombinationMethod1, deliveryMethod1)
readerPackage1 = EventReaderPackage(counterBuilder1, collector1)

outPath2 = os.path.join(args.outdir, 'tbl_jetpt.txt')
binning2 = RoundLog(0.1, 0)
keyComposer2 = GenericKeyComposer(('jet_pt', ), (binning2, ), (0, ))
counterBuilder2 = CounterBuilder(Counts, ('jet_pt', ), keyComposer2)
resultsCombinationMethod2 = CombineIntoPandasDataFrame()
deliveryMethod2 = WritePandasDataFrameToFile(outPath2)
collector2 = Collector(resultsCombinationMethod2, deliveryMethod2)
readerPackage2 = EventReaderPackage(counterBuilder2, collector2)

outPath3 = os.path.join(args.outdir, 'tbl_njets_nbjets.txt')
binning31 = Echo()
binning32 = Echo()
keyComposer3 = GenericKeyComposer(('nJet40', 'nBJet40'), (binning31, binning32))
counterBuilder3 = CounterBuilder(Counts, ('njets', 'nbjets'), keyComposer3)
resultsCombinationMethod3 = CombineIntoPandasDataFrame()
deliveryMethod3 = WritePandasDataFrameToFile(outPath3)
collector3 = Collector(resultsCombinationMethod3, deliveryMethod3)
readerPackage3 = EventReaderPackage(counterBuilder3, collector3)

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

progressBar = ProgressBar()
progressMonitor = MPProgressMonitor(progressBar)
eventLoopRunner = MPEventLoopRunner(8, progressMonitor)

readerBundle = EventReaderBundle(eventBuilder, eventLoopRunner, progressBar = progressBar)
readerBundle.addReaderPackage(readerPackage1)
readerBundle.addReaderPackage(readerPackage2)
readerBundle.addReaderPackage(readerPackage3)

heppyResultReader = HeppyResultReader()
heppyResultReader.addReader(readerBundle)

heppyResult = HeppyResult(args.heppydir)

heppyResultReader.read(heppyResult)

##__________________________________________________________________||
