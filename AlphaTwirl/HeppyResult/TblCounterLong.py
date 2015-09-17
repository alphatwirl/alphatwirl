# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os
from ReadCounter import ReadCounter

##__________________________________________________________________||
class TblCounterLong(object):

    """An alternative class to TblCounter.

    While TblCounter writes results in the wide format, this class writes
    results in the long format. Eventually, this class will replace TblCounter.


    Args:
        analyzerName (str): the name of the Heppy analyzer, e.g., skimAnalyzerCount
        fileName (str): the name of the counter file, e.g., SkimReport.txt
        outPath (str): a path to the output file

    """
    def __init__(self, analyzerName, fileName, outPath):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self._outPath = outPath
        self._readCounter = ReadCounter()
        self._rows = [['component', 'level', 'count']]

    def begin(self): pass

    def read(self, component):
        try:
            path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        except AttributeError, e:
            import logging
            logging.warning(e)
            return

        counter = self._readCounter(path)

        for level, var in counter.items():
            # quote if space is in a level, e.g., "Sum Weights"
            if ' ' in level: level =  '"' + level + '"'
            self._rows.append([component.name, level, var['count']])

    def end(self):
        f = self._open(self._outPath)
        f.write(listToAlignedText(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
