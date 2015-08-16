# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os

##____________________________________________________________________________||
class TblXsec(object):
    def __init__(self, outPath):
        self._outPath = outPath
        self._rows = [['component', 'xsec']]

    def begin(self): pass

    def read(self, component):
        xsec = component.config()['xSection']
        self._rows.append([component.name, xsec])

    def end(self):
        f = self._open(self._outPath)
        f.write(listToAlignedText(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##____________________________________________________________________________||
