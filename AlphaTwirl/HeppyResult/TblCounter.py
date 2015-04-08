# Tai Sakuma <tai.sakuma@cern.ch>
import os
import pandas
from ReadCounter import ReadCounter

##____________________________________________________________________________||
class TblCounter(object):
    def __init__(self, outPath, columnNames, analyzerName, fileName, levels):
        self._outPath = outPath
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.levels = levels
        self.columnNames = columnNames
        self._tbl = pandas.DataFrame()
        self._readCounter = ReadCounter()

    def begin(self): pass

    def read(self, component):
        path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
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
