#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import sys
from optparse import OptionParser

import AlphaTwirl

##__________________________________________________________________||
ROOT.gROOT.SetBatch(1)

##__________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/201525_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", default = -1, action = "store", type = 'long', help = "maximum number of events to process")
parser.add_option("-t", "--treeName", default = 'tree', action = "store", type = 'string', help = "the name of the tree")
(options, args) = parser.parse_args(sys.argv)

##__________________________________________________________________||
file = ROOT.TFile.Open(options.inputPath)
tree = file.Get(options.treeName)
events = AlphaTwirl.Events.Events(tree, options.nevents)

varNames = ('nJet40', 'nBJetTight40')
binnings = (AlphaTwirl.Binning.Echo(), AlphaTwirl.Binning.Echo())
keyComposer = AlphaTwirl.Counter.GenericKeyComposer(varNames, binnings)
countMethod = AlphaTwirl.Counter.Counts()
counter = AlphaTwirl.Counter.Counter(keyComposer, countMethod)

for event in events:
    counter.event(event)

print counter.results()

##__________________________________________________________________||
