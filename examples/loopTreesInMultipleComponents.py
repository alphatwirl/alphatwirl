#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import os
import sys
from optparse import OptionParser

import AlphaTwirl

##____________________________________________________________________________||
ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputDir', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14//201525_SingleMu', action = 'store', type = 'string', help = "the Heppy out dir")
parser.add_option("-n", "--nevents", default = -1, action = "store", type = 'long', help = "maximum number of events to process")
parser.add_option('-a', '--analyzerName', default = 'treeProducerSusyAlphaT', action = 'store', type = 'string', help = "the name of the Heppy analyzer that contains the root file")
parser.add_option('-r', '--rootFileName', default = 'tree.root', action = 'store', type = 'string', help = "the name of the root file that contains the tree")
parser.add_option("-t", "--treeName", default = 'tree', action = "store", type = 'string', help = "the name of the tree")
(options, args) = parser.parse_args(sys.argv)

##____________________________________________________________________________||
heppyResult = AlphaTwirl.HeppyResult.HeppyResult(options.inputDir)
for component in heppyResult.components():
    analyzer = getattr(component, options.analyzerName)
    inputPath = os.path.join(analyzer.path, options.rootFileName)
    file = ROOT.TFile.Open(inputPath)
    tree = file.Get(options.treeName)
    events = AlphaTwirl.Events.Events(tree, options.nevents)
    for event in events:
        run = event.run
        lumi = event.lumi
        eventId = event.evt
        print '%35s %6d %10d %9d' % (component.name, run, lumi, eventId),
        print

##____________________________________________________________________________||
