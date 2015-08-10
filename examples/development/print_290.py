#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.Counter import Counts
from AlphaTwirl.Binning import RoundLog, Echo
import AlphaTwirl

##__________________________________________________________________||
alphaTwirl = AlphaTwirl.AlphaTwirl()

tblcfg = [
    dict(outFileName = 'tbl_met.txt',
         branchNames = ('met_pt', ),
         outColumnNames = ('met', ),
         binnings = (RoundLog(0.1, 1), ),
         countsClass = Counts),
    dict(outFileName = 'tbl_jetpt.txt',
         branchNames = ('jet_pt', ),
         binnings = (RoundLog(0.1, 1), ),
         indices = (0, ),
         countsClass = Counts),
    dict(outFileName = 'tbl_njets_nbjets.txt',
         branchNames = ('nJet40', 'nBJet40'),
         outColumnNames = ('njets', 'nbjets'),
         binnings = (Echo(), Echo()),
         countsClass = Counts),
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
