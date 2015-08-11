#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl.HeppyResult import HeppyResult, EventBuilder
from AlphaTwirl.Counter import Counts

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--heppydir', default = '/Users/sakuma/work/cms/c150130_RA1_data/74X/MC/20150720_MC/20150720_SingleMu', help = "Heppy results dir")
parser.add_argument('-o', '--outdir', default = 'tmp')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'
outPath = os.path.join(args.outdir, 'tbl_met.txt')

eventBuilder = EventBuilder(analyzerName, fileName, treeName, args.nevents)

outFile = open(outPath, 'w')
columnnames = ("component", "met", "n", "nvar")
print >>outFile, "{:>22s} {:>12s} {:>6s} {:>6s}".format(*columnnames)

heppyResult = HeppyResult(args.heppydir)
for component in heppyResult.components():

    boundaries = [10**(i*0.1) for i in range(-10, 36)]
    counts = Counts()

    events = eventBuilder.build(component)
    for event in events:

        met = event.met_pt
        met_bin = max([b for b in boundaries if b < met])

        counts.count(met_bin)

    results = counts.results()
    keys = results.keys()
    keys.sort()
    for k in  keys:
        row = (component.name, k, results[k]['n'], results[k]['nvar'])
        print >>outFile, "{:>22s} {:12.6f} {:6.0f} {:6.0f}".format(*row)

##__________________________________________________________________||
