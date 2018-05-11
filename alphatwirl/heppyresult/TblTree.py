# Tai Sakuma <tai.sakuma@gmail.com>
from ..misc import mkdir_p
from ..misc import list_to_aligned_text
import os
import ROOT

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class TblTree(object):
    def __init__(self, analyzerName, fileName, treeName, outPath):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self.outPath = outPath
        self._rows = [
            ['component', 'n',
             'size', 'uncompressed_size', 'compression_factor',
             'analyzer', 'file', 'tree',
            ]]

    def begin(self): pass

    def read(self, component):
        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)

        size = tree.GetDirectory().GetKey(tree.GetName()).GetNbytes()
        size += tree.GetZipBytes()
        size /= 1024.0*1024.0 # MB
        uncompressed_size = tree.GetDirectory().GetKey(tree.GetName()).GetKeylen()
        uncompressed_size += tree.GetTotBytes()
        uncompressed_size /= 1024.0*1024.0 # MB
        compression_factor = uncompressed_size/size if size > 0 else 0

        size = round(size, 3)
        uncompressed_size = round(uncompressed_size, 3)
        compression_factor = round(compression_factor, 3)

        row = [component.name, tree.GetEntries(),
               size, uncompressed_size, compression_factor,
               self.analyzerName, self.fileName, self.treeName]
        self._rows.append(row)

    def end(self):
        f = self._open(self.outPath)
        f.write(list_to_aligned_text(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
