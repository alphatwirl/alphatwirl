#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT

##__________________________________________________________________||
inputPath = '/Users/sakuma/work/cms/c150130_RA1_data/74X/MC/20150720_MC/20150720_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root'
treeName = 'tree'
outPath = 'tmp/tbl_met.txt'

inputFile = ROOT.TFile.Open(inputPath)
tree = inputFile.Get(treeName)

boundaries = [10**(i*0.1) for i in range(-10, 36)]
counts = { }

for i in xrange(tree.GetEntries()):
    if tree.GetEntry(i) <= 0: break

    met = tree.met_pt
    met_bin = max([b for b in boundaries if b <= met])

    if not met_bin in counts: counts[met_bin] = 0
    counts[met_bin] += 1

keys = counts.keys()
keys.sort()
outFile = open(outPath, 'w')
print >>outFile, "{:>11s} {:>6s}".format("met", "n")
for k in  keys:
    print >>outFile, "{:11.6f} {:6d}".format(k, counts[k])

##__________________________________________________________________||
