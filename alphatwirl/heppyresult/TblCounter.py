# Tai Sakuma <tai.sakuma@gmail.com>
import os

from ..misc import mkdir_p
from ..misc import list_to_aligned_text
from .ReadCounter import ReadCounter

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class TblCounter(object):
    """This class reads counter files of HeppyResult.

    Args:
        analyzerName (str): the name of the Heppy analyzer, e.g., skimAnalyzerCount
        fileName (str): the name of the counter file, e.g., SkimReport.txt
        outPath (str): a path to the output file
        levels (list): a list of the levels to read. If not given, all levels will be read
        columnNames (list): a list of the column names of the output file. If not given, the levels will be used
    """
    def __init__(self, analyzerName, fileName, outPath, levels = None, columnNames = None):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self._outPath = outPath
        self.levels = levels
        self.columnNames = columnNames

        self._readCounter = ReadCounter()

        if self.levels is not None:
            self._determine_columnNames_start_rows()

    def begin(self): pass

    def read(self, component):
        try:
            path = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        except AttributeError as e:
            import logging
            logging.warning(e)
            return

        counter = self._readCounter(path)

        if self.levels is None:
            self.levels = counter.keys()
            self._determine_columnNames_start_rows()

        row = [component.name]
        for level, column in zip(self.levels, self.columnNames):
            row.append(counter[level]['count'])
        self._rows.append(row)

    def end(self):
        if self.levels is None:
            self._rows = [['component']]

        f = self._open(self._outPath)
        f.write(list_to_aligned_text(self._rows).encode())
        self._close(f)

    def _determine_columnNames_start_rows(self):
        if self.columnNames is None:
            self.columnNames = self.levels
        self._rows = [['component'] + list(self.columnNames)]


    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
