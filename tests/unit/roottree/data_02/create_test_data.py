#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
import os
import array
import numpy as np

import ROOT

##__________________________________________________________________||
def main():

    np.random.seed(0)

    create_file('sample_chain_01.root', nevents=1000)
    create_file('sample_chain_02.root', nevents=1000)
    create_file('sample_chain_03_zombie.root', nevents=1000)
    create_file('sample_chain_04.root', nevents=1000)
    make_zombie('sample_chain_03_zombie.root')

def create_file(name, nevents):

    ##
    max_njets = 30
    min_jet_pt = 20

    ievent_array = array.array('i', [0])
    njets_array = array.array('i', [0])
    met_array = array.array('f', [0])
    jet_pt_array = array.array('f', max_njets*[0])
    jet_eta_array = array.array('f', max_njets*[0])

    ##
    f = ROOT.TFile(name, 'recreate')
    t = ROOT.TTree('tree', 'sample tree')
    t.Branch('ievent', ievent_array, 'ievent/I')
    t.Branch('met', met_array, 'met/F')
    t.Branch('njets', njets_array, 'njets/I')
    t.Branch('jet_pt', jet_pt_array, 'jet_pt[njets]/F')
    t.Branch('jet_eta', jet_eta_array, 'jet_eta[njets]/F')

    for i in range(nevents):
        met = np.random.exponential(scale=100)
        njets = min(np.random.poisson(lam=4), max_njets)
        jet_pt = np.random.exponential(scale=100, size=njets) + min_jet_pt
        jet_pt[::-1].sort()
        jet_eta = np.random.normal(loc=0.0, scale=1.5, size=njets)

        ievent_array[0] = i
        njets_array[0] = njets
        met_array[0] = met
        jet_pt_array[:njets] = array.array('f', jet_pt)
        jet_eta_array[:njets] = array.array('f', jet_eta)

        t.Fill()

    t.Write()

def make_zombie(name):
    size = os.path.getsize(name)
    size_to_copy = int(size/2) # copy only the first half
    with open(name,'rb') as f:
        buf = f.read(size_to_copy)
    with open(name,'wb') as f:
        f.write(buf)

##__________________________________________________________________||
if __name__ == '__main__':
    main()

##__________________________________________________________________||
