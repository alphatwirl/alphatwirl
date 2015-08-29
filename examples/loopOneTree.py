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

for event in events:
    run = event.run
    lumi = event.lumi
    eventId = event.evt
    print '%6d %10d %9d' % (run, lumi, eventId),
    print

##__________________________________________________________________||
