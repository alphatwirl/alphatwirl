#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>

import array
import ROOT

##__________________________________________________________________||
def main():

    file_name = 'sample_chain_01.root'
    content_list = [
        [10, 20, 30],
        [24, 5]
    ]
    create_file(file_name, content_list)

    file_name = 'sample_chain_02.root'
    content_list = [
        [3, 10],
        [5, 8, 32, 15, 2],
        [22, 11],
    ]
    create_file(file_name, content_list)

    file_name = 'sample_chain_03.root'
    content_list = [
        [2, 7],
        [10, 100],
    ]
    create_file(file_name, content_list)

def create_file(name, contents):

    f = ROOT.TFile(name, 'recreate')
    t = ROOT.TTree('tree', 'sample tree')

    max_nvar = 128;
    nvar = array.array('i', [0])
    var = array.array('i', max_nvar*[0])

    t.Branch('nvar', nvar, 'nvar/I')
    t.Branch('var', var, 'var[nvar]/I')

    for c in contents:
        nvar[0] = len(c)
        for i, v in enumerate(c):
            var[i] = v
        t.Fill()

    t.Write()

##__________________________________________________________________||
if __name__ == '__main__':
    main()

##__________________________________________________________________||
