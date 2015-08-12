#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import CombineIntoList, WriteListToFile
from AlphaTwirl.HeppyResult import HeppyResult, EventBuilder
from AlphaTwirl.Counter import Counts, GenericKeyComposer, Counter
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.EventReader import Collector
from AlphaTwirl.ProgressBar import ProgressBar, ProgressReport

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/74X/MC/20150720_MC/20150720_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'

outPath1 = os.path.join(args.outdir, 'tbl_met.txt')
binning1 = RoundLog(0.1, 1)
keyComposer1 = GenericKeyComposer(('met_pt', ), (binning1, ))
resultsCombinationMethod1 = CombineIntoList(('met', ))
deliveryMethod1 = WriteListToFile(outPath1)
collector1 = Collector(resultsCombinationMethod1, deliveryMethod1)

outPath2 = os.path.join(args.outdir, 'tbl_jetpt.txt')
binning2 = RoundLog(0.1, 1)
keyComposer2 = GenericKeyComposer(('jet_pt', ), (binning2, ), (0, ))
resultsCombinationMethod2 = CombineIntoList(('jet_pt', ))
deliveryMethod2 = WriteListToFile(outPath2)
collector2 = Collector(resultsCombinationMethod2, deliveryMethod2)

outPath3 = os.path.join(args.outdir, 'tbl_njets_nbjets.txt')
binning31 = Echo()
binning32 = Echo()
keyComposer3 = GenericKeyComposer(('nJet40', 'nBJet40'), (binning31, binning32))
resultsCombinationMethod3 = CombineIntoList(('njets', 'nbjets'))
deliveryMethod3 = WriteListToFile(outPath3)
collector3 = Collector(resultsCombinationMethod3, deliveryMethod3)

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

progressBar = ProgressBar()

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    counts1 = Counts()
    counter1 = Counter(keyComposer1, counts1)
    collector1.addReader(component.name, counter1)

    counts2 = Counts()
    counter2 = Counter(keyComposer2, counts2)
    collector2.addReader(component.name, counter2)

    counts3 = Counts()
    counter3 = Counter(keyComposer3, counts3)
    collector3.addReader(component.name, counter3)

    events = eventBuilder.build(component)
    for event in events:

        report = ProgressReport(component.name, event.iEvent + 1, event.nEvents)
        progressBar.present(report)

        counter1.event(event)
        counter2.event(event)
        counter3.event(event)

collector1.collect()
collector2.collect()
collector3.collect()

##__________________________________________________________________||
