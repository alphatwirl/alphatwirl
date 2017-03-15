#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import timeit
import array
import ROOT
from AlphaTwirl.Events import Events, BEvents

##__________________________________________________________________||
inputPath = '/Users/sakuma/work/cms/c150130_RA1_data/80X/MC/20160708_B01_MCMiniAODv2_SM/AtLogic_MCMiniAODv2_SM/TTJets_HT2500toInf_madgraphMLM/treeProducerSusyAlphaT/tree.root'
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
def use_SetBranchAddress():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("njet", 1)
    tree.SetBranchStatus("jet_pt", 1)
    maxn = 65536
    njet = array.array('i',[ 0 ])
    jet_pt = array.array('d', maxn*[ 0 ])
    tree.SetBranchAddress("njet" , njet)
    tree.SetBranchAddress("jet_pt" , jet_pt)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        for i in range(njet[0]):
            jet_pt[i]

##__________________________________________________________________||
ways = ['use_Events', 'use_BEvents', 'use_SetBranchAddress']

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
