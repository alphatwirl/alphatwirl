# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os
from ReadCounter import ReadCounter

##__________________________________________________________________||
class TblBrilCalc(object):
    """This class reads brilcalc results in csv.

    Args:
        outPath (str): a path to the output file
        csvFileName (str): the name of the CSV file with the brilcalc results
    """
    def __init__(self, outPath, csvFileName = 'brilcalc.csv'):
        self._outPath = outPath
        self._csvFileName = csvFileName
        self._rows = [['component', 'delivered', 'recorded']]

    def begin(self): pass

    def read(self, component):

        path = os.path.join(component.path, self._csvFileName)

        try:
            csvfile = filter(lambda row: row[0]!='#', open(path))
        except IOError, e:
            import logging
            logging.warning(e)
            return

        import csv
        fieldnames = ('runfill', 'time', 'nls', 'ncms', 'delivered', 'recorded')
        lumi_csv = csv.DictReader(csvfile, fieldnames)
        lumi_csv = [l for l in lumi_csv] # read all
        delivered = [l['delivered'] for l in lumi_csv]
        delivered = [float(l) for l in delivered] # /ub
        delivered = [l/1000000 for l in delivered] # /ub
        delivered = sum(delivered)

        recorded = [l['recorded'] for l in lumi_csv]
        recorded = [float(l) for l in recorded] # /ub
        recorded = [l/1000000 for l in recorded] # /ub
        recorded = sum(recorded)

        row = [component.name, delivered, recorded]
        self._rows.append(row)

    def end(self):
        f = self._open(self._outPath)
        f.write(listToAlignedText(self._rows))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
