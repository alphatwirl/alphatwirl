# Tai Sakuma <tai.sakuma@gmail.com>
import os

from ..misc import mkdir_p
from ..misc import list_to_aligned_text
from .ReadCounter import ReadCounter

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class TblCounterLong(object):

    """An alternative class to TblCounter.

    While TblCounter writes results in the wide format, this class writes
    results in the long format. Eventually, this class will replace TblCounter.


    Args:
        analyzerName (str): the name of the Heppy analyzer, e.g., skimAnalyzerCount
        fileName (str): the name of the counter file, e.g., SkimReport.txt
        outPath (str): a path to the output file
        levels (list): a list of the levels to read. If not given, all levels will be read
        columnNames (list): a list of the column names of the output file. the default is ('component', 'level', 'count')

    """
    def __init__(self, analyzerName, fileName, outPath, levels = None, columnNames = ('component', 'level', 'count')):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self._outPath = outPath
        self.levels = levels

        self._readCounter = ReadCounter()
        self._rows = [columnNames]

    def begin(self): pass

    def read(self, component):
        try:
            path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        except AttributeError as e:
            import logging
            logging.warning(e)
            return

        counter = self._readCounter(path)

        for level, var in counter.items():
            if not self.levels is None and not level in self.levels: continue
            self._rows.append([component.name, level, var['count']])

    def end(self):
        f = self._open(self._outPath)
        f.write(list_to_aligned_text(self._rows).encode())
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
