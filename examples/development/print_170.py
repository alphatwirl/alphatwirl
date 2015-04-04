#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import EventBuilder, CombineIntoPandasDataFrame, WritePandasDataFrameToFile
from AlphaTwirl.HeppyResult import HeppyResult
from AlphaTwirl.Counter import Counts, GenericKeyComposer, Counter
from AlphaTwirl.Binning import RoundLog
from AlphaTwirl.EventReader import Collector

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
resultsCombinationMethod1 = CombineIntoPandasDataFrame()
deliveryMethod1 = WritePandasDataFrameToFile(outPath1)
collector1 = Collector(resultsCombinationMethod1, deliveryMethod1)

outPath2 = os.path.join(args.outdir, 'tbl_jetpt.txt')
binning2 = RoundLog(0.1, 0)
keyComposer2 = GenericKeyComposer(('jet_pt', ), (binning2, ), (0, ))
resultsCombinationMethod2 = CombineIntoPandasDataFrame()
deliveryMethod2 = WritePandasDataFrameToFile(outPath2)
collector2 = Collector(resultsCombinationMethod2, deliveryMethod2)

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    counts1 = Counts()
    counter1 = Counter(('met', ), keyComposer1, counts1)
    collector1.addReader(component.name, counter1)

    counts2 = Counts()
    counter2 = Counter(('jet_pt', ), keyComposer2, counts2)
    collector2.addReader(component.name, counter2)

    events = eventBuilder.build(component)
    for event in events:
        counter1.event(event)
        counter2.event(event)

collector1.collect()
collector2.collect()

##__________________________________________________________________||
