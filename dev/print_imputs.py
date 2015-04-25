#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import argparse

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputPath', default = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/20150331_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root')
parser.add_argument("-n", "--nevents", default = -1, type = int)
args = parser.parse_args()

##__________________________________________________________________||

inputFile = ROOT.TFile.Open(args.inputPath)
tree = inputFile.Get('tree')

tree.SetBranchStatus("*", 0)
tree.SetBranchStatus("met_pt", 1)

nevents = min(tree.GetEntries(), args.nevents) if args.nevents >= 0 else tree.GetEntries()
for i in xrange(nevents):
    if tree.GetEntry(i) <= 0: break
    print tree.met_pt

##__________________________________________________________________||
