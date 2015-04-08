# Tai Sakuma <tai.sakuma@cern.ch>
import os
import pandas
from HeppyResult import ReadCounter

##____________________________________________________________________________||
class TblNevt(object):
    def __init__(self, outPath):
        self._outPath = outPath
        self._tbl = pandas.DataFrame()
        self.levels = ('All Events', 'Sum Weights')
        self.columnNames = ('nevt', 'nevt_sumw')
        self._readCounter = ReadCounter()

    def begin(self): pass

    def read(self, component):
        path = os.path.join(component.skimAnalyzerCount.path, 'SkimReport.txt')
        counter = self._readCounter(path)
        df_data = {'component': (component.name, )}
        for level, column in zip(self.levels, self.columnNames):
            df_data[column] = (counter[level]['count'], )
        df = pandas.DataFrame(df_data)
        self._tbl = self._tbl.append(df)

    def end(self):
        f = self._open(self._outPath)
        if len(self._tbl.index) == 0:
            f.write('component ' + " ".join(self.columnNames) + '\n')
        else:
            self._tbl.to_string(f, index = False, float_format = '{:.3f}'.format)
            f.write('\n')
        self._close(f)

    def _open(self, path): return open(path, 'w')
    def _close(self, file): file.close()

##____________________________________________________________________________||
