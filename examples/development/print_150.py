#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl import CombineIntoList, WriteListToFile
from AlphaTwirl.HeppyResult import HeppyResult, EventBuilder
from AlphaTwirl.Counter import Counts, GenericKeyComposer, Counter
from AlphaTwirl.Binning import RoundLog

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/20150331_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'
outPath = os.path.join(args.outdir, 'tbl_met.txt')

binning = RoundLog(0.1, 0)
keyComposer = GenericKeyComposer(('met_pt', ), (binning, ))
resultsCombinationMethod = CombineIntoList(('met', ))
deliveryMethod = WriteListToFile(outPath)
datasetReaderPairs = [ ]

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    counts = Counts()
    counter = Counter(keyComposer, counts)

    datasetReaderPairs.append((component.name, counter))

    events = eventBuilder.build(component)
    for event in events:

        counter.event(event)

results = resultsCombinationMethod.combine(datasetReaderPairs)
deliveryMethod.deliver(results)

##__________________________________________________________________||
