#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
from optparse import OptionParser

import AlphaTwirl

##____________________________________________________________________________||
ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/201525_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", default = -1, action = "store", type = 'long', help = "maximum number of events to process")
parser.add_option("-t", "--treeName", default = 'tree', action = "store", type = 'string', help = "the name of the tree")
(options, args) = parser.parse_args(sys.argv)

##____________________________________________________________________________||
file = ROOT.TFile.Open(options.inputPath)
tree = file.Get(options.treeName)
events = AlphaTwirl.Events(tree, options.nevents)

counter_nvtx = AlphaTwirl.Counter_nvtx()

for event in events:
    run = event.run
    lumi = event.lumi
    eventId = event.evt
    print '%6d %10d %9d' % (run, lumi, eventId),
    print
    counter_nvtx.event(event)

print counter_nvtx.results()

##____________________________________________________________________________||
