#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import pandas as pd

from AlphaTwirl.Aggregate import combine_MC_yields_in_datasets_into_xsec_in_processes

##__________________________________________________________________||
def main():
    tbl_xsec = pd.read_table('tbl_xsec.txt', delim_whitespace = True)
    tbl_nevt = pd.read_table('tbl_nevt.txt', delim_whitespace = True)
    tbl_process = pd.read_table('tbl_process.txt', delim_whitespace = True)
    tbl_yield = pd.read_table('tbl_component_njets_HT_MET.txt', delim_whitespace = True)
    tbl_yield = tbl_yield[tbl_yield['njets'].isin([4, 5])]
    tbl_yield = tbl_yield[tbl_yield['HT'].isin([600, 800])]
    tbl_yield = tbl_yield[tbl_yield['MET'] < 150]
    tbl_yield = tbl_yield[tbl_yield['jet2pt'] == 100]
    tbl_yield = tbl_yield[tbl_yield['n'] > 0]
    components = ['QCD_HT_1000ToInf', 'QCD_HT_1000ToInf_ext1', 'QCD_HT_500To1000',
                  'TBar_tWch', 'T_tWch', 'TTJets']
    tbl_yield = tbl_yield[tbl_yield['component'].isin(components)]
    del tbl_yield['jet2pt']
    writeToFile(tbl_yield, 'tbl_in.txt')
    tbl_out = combine_MC_yields_in_datasets_into_xsec_in_processes(tbl_yield, tbl_process, tbl_nevt, tbl_xsec)
    writeToFile(tbl_out, 'tbl_out.txt')

##__________________________________________________________________||
def writeToFile(tbl, path):
    print 'writing ', path
    f = open(path, 'w')
    tbl.to_string(f, index = False)
    f.write("\n")
    f.close()

##__________________________________________________________________||
if __name__ == '__main__':
    main()
