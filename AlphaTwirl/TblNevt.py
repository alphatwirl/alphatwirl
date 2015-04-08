# Tai Sakuma <tai.sakuma@cern.ch>
from HeppyResult import TblCounter

##____________________________________________________________________________||
class TblNevt(object):
    def __init__(self, outPath):
        self.tblcounter = TblCounter(
            outPath,
            columnNames = ('nevt', 'nevt_sumw'),
            analyzerName = 'skimAnalyzerCount',
            fileName = 'SkimReport.txt',
            levels = ('All Events', 'Sum Weights')
        )

    def begin(self): self.tblcounter.begin()
    def read(self, component): self.tblcounter.read(component)
    def end(self): self.tblcounter.end()

##____________________________________________________________________________||
