# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os
import ROOT

##__________________________________________________________________||
class TblTreeEntries(object):
    def __init__(self, analyzerName, fileName, treeName, outPath, columnName = 'n'):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self.outPath = outPath
        self._rows = [['component', columnName]]

    def begin(self): pass

    def read(self, component):
        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)

        row = [component.name, tree.GetEntries()]
        self._rows.append(row)

    def end(self):
        f = self._open(self.outPath)
        f.write(listToAlignedText(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
