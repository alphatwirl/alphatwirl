#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import os
import argparse
from AlphaTwirl.HeppyResult import Component, EventBuilder

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
print >>outFile, "{:>22s} {:>12s} {:>6s}".format("component", "met", "n")

for componentName in os.listdir(args.heppydir):
    if componentName in ('Chunks', 'failed'): continue
    componentPath = os.path.join(args.heppydir, componentName)
    if not os.path.isdir(componentPath): continue
    component = Component(componentPath)

    boundaries = [10**(i*0.1) for i in range(-10, 36)]
    counts = { }

    for event in eventBuilder.build(component):

        met = event.met_pt
        met_bin = max([b for b in boundaries if b < met])

        if not met_bin in counts: counts[met_bin] = 0
        counts[met_bin] += 1

    keys = counts.keys()
    keys.sort()
    for k in  keys:
        print >>outFile, "{:>22s} {:12.6f} {:6d}".format(componentName, k, counts[k])

##__________________________________________________________________||
