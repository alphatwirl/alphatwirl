#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import os, sys
import tempfile

##__________________________________________________________________||
thisdir =  os.path.dirname(os.path.realpath(__file__))
alphatwirldir = os.path.dirname(thisdir)
sys.path.insert(1, alphatwirldir)
from AlphaTwirl.Counter import Counts
from AlphaTwirl.Binning import RoundLog, Echo
import AlphaTwirl

##__________________________________________________________________||
heppydir='/Users/sakuma/work/cms/c150130_RA1_data/PHYS14/20150507_SingleMu'
nevents=100000
outdir = tempfile.mkdtemp()
sys.argv.extend(["-i", heppydir, "-n", str(nevents), "-o", outdir])

##__________________________________________________________________||
alphaTwirl = AlphaTwirl.AlphaTwirl()

tblcfg = [
    dict(outFileName = 'tbl_met.txt',
         branchNames = ('met_pt', ),
         outColumnNames = ('met', ),
         binnings = (RoundLog(0.1, 0), ),
         countsClass = Counts),
    dict(outFileName = 'tbl_jetpt.txt',
         branchNames = ('jet_pt', ),
         binnings = (RoundLog(0.1, 0), ),
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

##__________________________________________________________________||
import cProfile, pstats, StringIO

pr = cProfile.Profile()
pr.enable()

alphaTwirl.run()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream = s).strip_dirs().sort_stats(sortby)
ps.print_stats()
print s.getvalue()

## cProfile.run("alphaTwirl.run()")

##__________________________________________________________________||
