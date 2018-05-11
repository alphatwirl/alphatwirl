# Tai Sakuma <tai.sakuma@gmail.com>
from ..misc import mkdir_p
from ..misc import list_to_aligned_text
import os
from .ReadCounter import ReadCounter

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class TblBrilCalc(object):
    """This class reads brilcalc results in csv.

    Args:
        outPath (str): a path to the output file
        csvFileName (str): the name of the CSV file with the brilcalc results
    """
    def __init__(self, outPath, csvFileName = 'brilcalc.csv'):
        self._outPath = outPath
        self._csvFileName = csvFileName
        self._rows = [['component', 'luminosity']]

    def begin(self): pass

    def read(self, component):

        path = os.path.join(component.path, self._csvFileName)

        if not os.path.exists(path): return

        try:
            csvfile = filter(lambda row: row[0]!='#', open(path))
        except IOError as e:
            import logging
            logging.warning(e)
            return

        import csv, re
        fieldnames = ('runfill', 'time', 'nls', 'ncms', 'delivered', 'recorded')
        lumi_csv = csv.DictReader(csvfile, fieldnames)
        lumi_csv = [l for l in lumi_csv] # read all
        lumi_csv = [l for l in lumi_csv if re.search(r'^[0-9]*:[0-9]*$', l['runfill'])] # e.g. '258159:4449' for the runfill field
        recorded = [l['recorded'] for l in lumi_csv]
        recorded = [float(l) for l in recorded] # /ub
        recorded = [l/1000000 for l in recorded] # /ub
        recorded = sum(recorded)

        row = [component.name, recorded]
        self._rows.append(row)

    def end(self):
        if len(self._rows) == 1: return

        f = self._open(self._outPath)
        f.write(list_to_aligned_text(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
