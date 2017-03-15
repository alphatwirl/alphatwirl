#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT
import os
import argparse

import AlphaTwirl

##__________________________________________________________________||
ROOT.gROOT.SetBatch(1)

##__________________________________________________________________||
default_input = '/afs/cern.ch/work/s/sakuma/public/cms/c150130_RA1_data/80X/MC/20160811_B01/ROC_MC_SM'

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-dir', default = default_input, help = "the Heppy out dir")
parser.add_argument("-n", "--nevents", default = -1, type = int, help = "maximum number of events to process")
parser.add_argument('-a', '--analyzer-name', default = 'roctree', help = "the name of the Heppy analyzer that contains the root file")
parser.add_argument('-r', '--rootfile-name', default = 'tree.root', help = "the name of the root file that contains the tree")
parser.add_argument("-t", "--tree-name", default = 'tree', help = "the name of the tree")
args = parser.parse_args()

##__________________________________________________________________||
heppyResult = AlphaTwirl.HeppyResult.HeppyResult(args.input_dir)
for component in heppyResult.components():
    analyzer = getattr(component, args.analyzer_name)
    input_path = os.path.join(analyzer.path, args.rootfile_name)
    file = ROOT.TFile.Open(input_path)
    tree = file.Get(args.tree_name)
    events = AlphaTwirl.Events.BEvents(tree, args.nevents)
    for event in events:
        print '{:>35}'.format(component.name),
        print '{:>6} {:>10} {:>9}'.format(event.run[0], event.lumi[0], event.evt[0]),
        print

##__________________________________________________________________||
