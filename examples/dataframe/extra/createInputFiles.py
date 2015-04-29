#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.Counter import Counts
from AlphaTwirl.Binning import RoundLog, Echo
from AlphaTwirl.HeppyResult import TblXsec, TblCounter
import AlphaTwirl
import os


##__________________________________________________________________||
alphaTwirl = AlphaTwirl.AlphaTwirl()

parser = alphaTwirl.ArgumentParser()
args = parser.parse_args()

##____________________________________________________________________________||
alphaTwirl.addComponentReader(TblXsec(os.path.join(args.outDir, 'tbl_xsec.txt')))

tblNevt = TblCounter(
    outPath = os.path.join(args.outDir, 'tbl_nevt.txt'),
    columnNames = ('nevt', ),
    analyzerName = 'skimAnalyzerCount',
    fileName = 'SkimReport.txt',
    levels = ('All Events', )
    )
alphaTwirl.addComponentReader(tblNevt)

##____________________________________________________________________________||
tblcfg = [
    dict(outFileName = 'tbl_component_met.txt',
         branchNames = ('met_pt', ),
         outColumnNames = ('met', ),
         binnings = (RoundLog(0.1, 0), ),
     )
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
import pandas as pd

##__________________________________________________________________||
d1 = pd.read_table(os.path.join(args.outDir, 'tbl_process.txt'), delim_whitespace = True)
d2 = pd.read_table(os.path.join(args.outDir, 'tbl_xsec.txt'), delim_whitespace = True)

d = pd.merge(d1, d2)
d = d[['phasespace', 'xsec']].drop_duplicates()

f = open(os.path.join(args.outDir, 'tbl_xsec.txt'), 'w')
d.to_string(f, index = False)
f.write("\n")
f.close()


##__________________________________________________________________||
