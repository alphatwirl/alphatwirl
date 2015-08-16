# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
import os
import ROOT

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
class TblBranch(object):
    def __init__(self, outPath, analyzerName, fileName, treeName):
        self.outPath = outPath
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self._done = False

    def begin(self): pass

    def read(self, component):
        if self._done: return
        self._done = True

        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)

        results = [ ]
        results.append(('name', 'type', 'isarray', 'countname'))
        for leaf in tree.GetListOfLeaves():
            leafcount = leaf.GetLeafCount()
            isArray = not IsROOTNullPointer(leafcount)
            row = [ ]
            row.append(leaf.GetName())
            row.append(leaf.GetTypeName())
            row.append('1' if isArray else '0')
            row.append(leafcount.GetName() if isArray else None)
            results.append(row)

        transposed = [[r[i] for r in results] for i in range(len(results[0]))]
        transposed = [[str(e) for e in r] for r in transposed]
        columnWidths = [max([len(e) for e in r]) for r in transposed]
        format = " {:>" + "s} {:>".join([str(e) for e in columnWidths]) + "s}"

        f = self._open(self.outPath)
        for row in zip(*transposed):
            f.write(format.format(*row))
            f.write("\n")
        self._close(f)

    def end(self): pass

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
