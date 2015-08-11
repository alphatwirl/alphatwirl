#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import os

##__________________________________________________________________||
heppyPath = '/Users/sakuma/work/cms/c150130_RA1_data/74X/MC/20150720_MC/20150720_SingleMu'
analyzerName = 'treeProducerSusyAlphaT'
fileName = 'tree.root'
treeName = 'tree'
outPath = 'tmp/tbl_met.txt'

outFile = open(outPath, 'w')
print >>outFile, "{:>22s} {:>12s} {:>6s}".format("component", "met", "n")

for component in os.listdir(heppyPath):
    if component in ('Chunks', 'failed'): continue
    componentPath = os.path.join(heppyPath, component)
    if not os.path.isdir(componentPath): continue
    analyzerPath = os.path.join(componentPath, analyzerName)
    inputPath = os.path.join(analyzerPath, fileName)

    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)

    boundaries = [10**(i*0.1) for i in range(-10, 36)]
    counts = { }

    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break

        met = tree.met_pt
        met_bin = max([b for b in boundaries if b < met])

        if not met_bin in counts: counts[met_bin] = 0
        counts[met_bin] += 1

    keys = counts.keys()
    keys.sort()
    for k in  keys:
        print >>outFile, "{:>22s} {:12.6f} {:6d}".format(component, k, counts[k])

##__________________________________________________________________||
