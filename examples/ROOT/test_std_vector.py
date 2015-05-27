#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import timeit
import array
import ROOT
from AlphaTwirl.Events import Events, BEvents

##__________________________________________________________________||
inputPath = 'tree.root'
treeName = 'tree'

##__________________________________________________________________||
def use_BEvents():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    events = BEvents(tree)
    jet_pt = events.jet_pt
    trigger_path = events.trigger_path
    trigger_version = events.trigger_version
    for event in events:
        for i in range(len(jet_pt)):
            jet_pt[i]
        # print [v for v in trigger_path]
        # print [v for v in trigger_version]

##__________________________________________________________________||
def use_SetBranchAddress():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("njet", 1)
    tree.SetBranchStatus("jet_pt", 1)
    tree.SetBranchStatus("trigger_path", 1)
    tree.SetBranchStatus("trigger_version", 1)
    maxn = 65536
    njet = array.array('i',[ 0 ])
    jet_pt = array.array('d', maxn*[ 0 ])
    tree.SetBranchAddress("njet" , njet)
    tree.SetBranchAddress("jet_pt" , jet_pt)
    trigger_path = ROOT.vector('string')()
    tree.SetBranchAddress("trigger_path", trigger_path)
    trigger_version = ROOT.vector('int')()
    tree.SetBranchAddress("trigger_version", trigger_version)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        for i in range(njet[0]):
            jet_pt[i]
        # print [v for v in trigger_path]
        # print [v for v in trigger_version]

##__________________________________________________________________||
ways = ['simplest_way', 'use_SetBranchStatus', 'use_GetLeaf', 'use_SetBranchAddress']
ways = ['use_BEvents', 'use_SetBranchAddress', 'use_BEvents', 'use_SetBranchAddress']

for w in ways:
    print w, ':',
    print timeit.timeit(w + '()', number = 1, setup = 'from __main__ import ' + w)

##__________________________________________________________________||
