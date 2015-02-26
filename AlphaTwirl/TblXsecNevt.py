# Tai Sakuma <sakuma@fnal.gov>
import os
import pandas

##____________________________________________________________________________||
class TblXsecNevt(object):
    def __init__(self, outPath):
        self._outPath = outPath
        self._tbl = pandas.DataFrame()

    def begin(self): pass

    def read(self, component):
        xsec = component.config()['xSection']
        nevt = getNEventsFor(component)
        self._tbl = self._tbl.append(pandas.DataFrame({'component': (component.name, ), 'xsec': (xsec, ), 'nevt': (nevt, )}))

    def end(self):
        self._tbl.nevt = self._tbl.nevt.apply(lambda x: '%.3f' % x)
        f = open(self._outPath, 'w')
        self._tbl.to_string(f, index = False)
        f.close()

##____________________________________________________________________________||
def getNEventsFor(component):
    file = open(os.path.join(component.skimAnalyzerCount.path, 'SkimReport.txt'))
    file.readline() # skip the 1st line
    lines = [l.strip() for l in file]
    lines = [l for l in lines if l.startswith('Sum Weights')]
    return float(lines[0][len('Sum Weights'):].strip().split()[0])

##____________________________________________________________________________||
