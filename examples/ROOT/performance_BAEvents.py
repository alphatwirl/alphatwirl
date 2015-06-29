#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import timeit
import array
import ROOT
from AlphaTwirl.Events import Events, BEvents

##__________________________________________________________________||
inputPath = '/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/20150331_SingleMu/TTJets/treeProducerSusyAlphaT/tree.root'
treeName = 'tree'

##__________________________________________________________________||
def use_Events():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("jet_pt", 1)
    events = Events(tree)
    for event in events:
        jet_pt = event.jet_pt
        for i in range(len(jet_pt)):
            jet_pt[i]

##__________________________________________________________________||
def use_BEvents():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    events = BEvents(tree)
    jet_pt = events.jet_pt
    for event in events:
        for i in range(len(jet_pt)):
            jet_pt[i]

##__________________________________________________________________||
class ABranch(object):
    def __init__(self, event):
        self.mht40_pt = event.mht40_pt
        self.met_pt = event.met_pt

    def __getitem__(self, i):
        if 0 != i:
            raise IndexError("the index should be zero for this branch: " + self.name + "[" + str(i) + "]")
        return self.mht40_pt[0]/self.met_pt[0]

##__________________________________________________________________||
def use_BAEvents():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    events = BEvents(tree)
    mht40_pt = events.mht40_pt
    met_pt = events.met_pt
    events.mhtomet = ABranch(events)
    mhtomet = events.mhtomet
    for event in events:
        print mht40_pt[0]/met_pt[0], mhtomet[0], events.mhtomet[0]

##__________________________________________________________________||
# ways = ['use_Events', 'use_BEvents', 'use_BAEvents']
ways = ['use_BAEvents']

for w in ways:
    print w, ':',
    print timeit.timeit(w + '()', number = 1, setup = 'from __main__ import ' + w)

##__________________________________________________________________||
# import cProfile, pstats, StringIO
# pr = cProfile.Profile()
# pr.enable()
#
# use_BEvents()
#
# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream = s).strip_dirs().sort_stats(sortby)
# ps.print_stats()
# print s.getvalue()

##__________________________________________________________________||
