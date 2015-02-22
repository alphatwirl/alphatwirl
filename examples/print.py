#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
import math
import json
import re
import os
from optparse import OptionParser

import AlphaTwirl

##____________________________________________________________________________||
ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputDir', default = '/afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/201525_SingleMu', action = 'store', type = 'string')
parser.add_option("-n", "--nevents", action = "store", default = -1, type = 'long', help = "maximum number of events to process")
(options, args) = parser.parse_args(sys.argv)

##____________________________________________________________________________||
def main():

    heppy = AlphaTwirl.HeppyResult.HeppyResult(options.inputDir)
    for component in heppy.components():
        print component.name
        inputPath = os.path.join(component.treeProducerSusyAlphaT.path, 'tree.root')
        print inputPath
        count(inputPath)

##____________________________________________________________________________||
def count(inputPath):

    events = buildEvents(inputPath, maxEvents = options.nevents, treeName = "tree")

    for event in events:

        run = event.run
        lumi = event.lumi
        eventId = event.evt
        print '%6d %10d %9d' % (run, lumi, eventId),
        print 

    return

##____________________________________________________________________________||
def buildEvents(inputPath, maxEvents, treeName):
    file = ROOT.TFile.Open(inputPath)
    tree = file.Get(treeName)
    return AlphaTwirl.Events(tree, maxEvents)

##____________________________________________________________________________||
if __name__ == '__main__':
    main()
