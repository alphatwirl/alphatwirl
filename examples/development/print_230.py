#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import CombineIntoList, WriteListToFile
from AlphaTwirl.HeppyResult import HeppyResult, EventBuilder
from AlphaTwirl.Counter import Counts, GenericKeyComposerBuilder, CounterBuilder
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.EventReader import Collector, EventReaderPackage
from AlphaTwirl.ProgressBar import ProgressBar, ProgressReport, ProgressMonitor

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/20150331_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'

outPath1 = os.path.join(args.outdir, 'tbl_met.txt')
binning1 = RoundLog(0.1, 0)
keyComposer1 = GenericKeyComposerBuilder(('met_pt', ), (binning1, ))
counterBuilder1 = CounterBuilder(Counts, ('met', ), keyComposer1)
resultsCombinationMethod1 = CombineIntoList()
deliveryMethod1 = WriteListToFile(outPath1)
collector1 = Collector(resultsCombinationMethod1, deliveryMethod1)
readerPackage1 = EventReaderPackage(counterBuilder1, collector1)

outPath2 = os.path.join(args.outdir, 'tbl_jetpt.txt')
binning2 = RoundLog(0.1, 0)
keyComposer2 = GenericKeyComposerBuilder(('jet_pt', ), (binning2, ), (0, ))
counterBuilder2 = CounterBuilder(Counts, ('jet_pt', ), keyComposer2)
resultsCombinationMethod2 = CombineIntoList()
deliveryMethod2 = WriteListToFile(outPath2)
collector2 = Collector(resultsCombinationMethod2, deliveryMethod2)
readerPackage2 = EventReaderPackage(counterBuilder2, collector2)

outPath3 = os.path.join(args.outdir, 'tbl_njets_nbjets.txt')
binning31 = Echo()
binning32 = Echo()
keyComposer3 = GenericKeyComposerBuilder(('nJet40', 'nBJet40'), (binning31, binning32))
counterBuilder3 = CounterBuilder(Counts, ('njets', 'nbjets'), keyComposer3)
resultsCombinationMethod3 = CombineIntoList()
deliveryMethod3 = WriteListToFile(outPath3)
collector3 = Collector(resultsCombinationMethod3, deliveryMethod3)
readerPackage3 = EventReaderPackage(counterBuilder3, collector3)

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

class AllEvents(object):
    def __call__(self, event): return True

eventSelection = AllEvents()

progressBar = ProgressBar()
progressMonitor = ProgressMonitor(progressBar)
progressReporter = progressMonitor.createReporter()

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    reader1 = readerPackage1.make(component.name)
    reader2 = readerPackage2.make(component.name)
    reader3 = readerPackage3.make(component.name)

    events = eventBuilder.build(component)
    for event in events:

        report = ProgressReport(component.name, event.iEvent + 1, event.nEvents)
        progressReporter.report(report)

        if not eventSelection(event): continue

        reader1.event(event)
        reader2.event(event)
        reader3.event(event)

readerPackage1.collect()
readerPackage2.collect()
readerPackage3.collect()

##__________________________________________________________________||
