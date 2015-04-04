#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.Counter import Counts
from AlphaTwirl.Binning import RoundLog, Echo
import AlphaTwirl

# ./example_alphatwirl_dev/print_290.py -i /Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/201525_SingleMu -n 10 --force
##__________________________________________________________________||
alphaTwirl = AlphaTwirl.AlphaTwirl()

tblcfg = [
    dict(outFilePath = 'tmp/tbl_met.txt', branchNames = ('met_pt', ), outColumnNames = ('met', ), binnings = (RoundLog(0.1, 0), ), countsClass = Counts),
    dict(outFilePath = 'tmp/tbl_jetpt.txt', branchNames = ('jet_pt', ), binnings = (RoundLog(0.1, 0), ), indices = (0, ), countsClass = Counts),
    dict(outFilePath = 'tmp/tbl_njets_nbjets.txt', branchNames = ('nJet40', 'nBJet40'), outColumnNames = ('njets', 'nbjets'), binnings = (Echo(), Echo()), countsClass = Counts),
]

alphaTwirl.addTreeReader(
    analyzerName = 'treeProducerSusyAlphaT',
    fileName = 'tree.root',
    treeName = 'tree',
    tableConfigs = tblcfg,
    eventSelection = None,
)

alphaTwirl.run()

##__________________________________________________________________||
