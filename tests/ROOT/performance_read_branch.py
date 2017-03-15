#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import timeit
import array
import ROOT

##__________________________________________________________________||
inputPath = '/Users/sakuma/work/cms/c150130_RA1_data/80X/MC/20160708_B01_MCMiniAODv2_SM/AtLogic_MCMiniAODv2_SM/TTJets_HT2500toInf_madgraphMLM/treeProducerSusyAlphaT/tree.root'
treeName = 'tree'

##__________________________________________________________________||
def simplest_way():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        tree.met_pt

##__________________________________________________________________||
def use_SetBranchStatus():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("met_pt", 1)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        tree.met_pt

##__________________________________________________________________||
def use_GetLeaf():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("met_pt", 1)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        tree.GetLeaf('met_pt').GetValue()

##__________________________________________________________________||
def use_SetBranchAddress():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("met_pt", 1)
    met_pt = array.array('d', [ 0 ])
    tree.SetBranchAddress("met_pt" , met_pt)
    for i in xrange(tree.GetEntries()):
        if tree.GetEntry(i) <= 0: break
        met_pt[0]

##__________________________________________________________________||
ways = ['simplest_way', 'use_SetBranchStatus', 'use_GetLeaf', 'use_SetBranchAddress']

for w in ways:
    print w, ':',
    print timeit.timeit(w + '()', number = 1, setup = 'from __main__ import ' + w)

##__________________________________________________________________||
