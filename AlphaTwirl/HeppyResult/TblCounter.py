# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os
from ReadCounter import ReadCounter

##____________________________________________________________________________||
class TblCounter(object):
    def __init__(self, outPath, columnNames, analyzerName, fileName, levels):
        self._outPath = outPath
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.levels = levels
        self.columnNames = columnNames
        self._readCounter = ReadCounter()
        self._rows = [['component'] + list(columnNames)]

    def begin(self): pass

    def read(self, component):
        path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        counter = self._readCounter(path)
        row = [component.name]
        for level, column in zip(self.levels, self.columnNames):
            row.append(counter[level]['count'])
        self._rows.append(row)

    def end(self):
        f = self._open(self._outPath)
        f.write(listToAlignedText(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##____________________________________________________________________________||
