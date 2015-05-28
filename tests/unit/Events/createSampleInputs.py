#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import argparse
import ROOT

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputpath', default = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/20150331_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root')
parser.add_argument('-t', '--treename', default = 'tree')
parser.add_argument('-o', '--outpath', default = 'tmp.root')
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process for each component")
args = parser.parse_args()

##__________________________________________________________________||
inputFile = ROOT.TFile.Open(args.inputpath)
tree = inputFile.Get(args.treename)
tree.SetBranchStatus("*", 0)
tree.SetBranchStatus("njet", 1)
tree.SetBranchStatus("jet_pt", 1)
tree.SetBranchStatus("met_pt", 1)

outFile = ROOT.TFile.Open(args.outpath, "RECREATE")
newtree = tree.CloneTree(0)

nevents = min(tree.GetEntries(), args.nevents) if args.nevents >= 0 else tree.GetEntries()
for i in xrange(nevents):
    if tree.GetEntry(i) <= 0: break
    newtree.Fill()

newtree.Write()
outFile.Close()



##__________________________________________________________________||
