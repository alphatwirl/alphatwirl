# Tai Sakuma <tai.sakuma@cern.ch>
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
        transposed = [[r[i] for r in self._rows] for i in range(len(self._rows[0]))]
        transposed = [[int(e) if isinstance(e, float) and e.is_integer() else e for e in r] for r in transposed]
        transposed = [[str(e) for e in r] for r in transposed]
        columnWidths = [max([len(e) for e in r]) for r in transposed]
        format = " {:>" + "s} {:>".join([str(e) for e in columnWidths]) + "s}"
        f = self._open(self._outPath)
        for row in zip(*transposed):
            f.write(format.format(*row))
            f.write("\n")
        self._close(f)

    def _open(self, path): return open(path, 'w')
    def _close(self, file): file.close()

##____________________________________________________________________________||
