#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import timeit
import array
import ROOT

from alphatwirl.events import Events, BEvents

# https://cp3.irmp.ucl.ac.be/projects/delphes/ticket/1039
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
ROOT.gSystem.Load("libDelphes.so")

##__________________________________________________________________||
inputPath = '/hdfs/user/ds13962/delphes_jobs/job_20170417_001/QCD_HT1000to1500/0000/delphes.root'
treeName = 'Delphes'

##__________________________________________________________________||
def use_Events():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    events = Events(tree)
    for event in events:
        for i in range(event.Jet.GetEntries()):
            event.Jet[i].PT

##__________________________________________________________________||
def use_Events_SetBranchStatus_var():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("Jet.PT", 1)
    events = Events(tree)
    for event in events:
        for i in range(event.Jet.GetEntries()):
            event.Jet[i].PT

##__________________________________________________________________||
def use_Events_SetBranchStatus_obj():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("Jet.*", 1)
    events = Events(tree)
    for event in events:
        for i in range(event.Jet.GetEntries()):
            event.Jet[i].PT

##__________________________________________________________________||
# https://github.com/delphes/delphes/blob/master/examples/Example1.py
def use_ExRootTreeReader():
    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    treeReader = ROOT.ExRootTreeReader(tree)
    nentries = treeReader.GetEntries()
    branchJet = treeReader.UseBranch("Jet")
    for ientry in range(nentries):
        treeReader.ReadEntry(ientry)
        for i in range(branchJet.GetEntries()):
            branchJet[i].PT

##__________________________________________________________________||
ways = [
    'use_Events',
    'use_Events_SetBranchStatus_var',
    'use_Events_SetBranchStatus_obj',
    'use_ExRootTreeReader'
]

for w in ways:
    print w, ':',
    print timeit.timeit(w + '()', number = 1, setup = 'from __main__ import ' + w)

##__________________________________________________________________||
# use_Events : 4.99250912666
# use_Events_SetBranchStatus_var : 0.321241855621
# use_Events_SetBranchStatus_obj : 0.540351867676
# use_ExRootTreeReader : 0.495839118958

##__________________________________________________________________||
