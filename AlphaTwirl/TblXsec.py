# Tai Sakuma <tai.sakuma@cern.ch>
import os
import pandas

##____________________________________________________________________________||
class TblXsec(object):
    def __init__(self, outPath):
        self._outPath = outPath
        self._tbl = pandas.DataFrame()

    def begin(self): pass

    def read(self, component):
        xsec = component.config()['xSection']
        self._tbl = self._tbl.append(pandas.DataFrame({'component': (component.name, ), 'xsec': (xsec, )}))

    def end(self):
        f = open(self._outPath, 'w')
        self._tbl.to_string(f, index = False)
        f.close()

##____________________________________________________________________________||
