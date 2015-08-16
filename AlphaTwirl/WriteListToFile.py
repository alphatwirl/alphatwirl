# Tai Sakuma <tai.sakuma@cern.ch>
from .mkdir_p import mkdir_p
import os

##__________________________________________________________________||
def listToAlignedText(src):

        # e.g.,
        # src = [
        #     ('component', 'v1', 'nvar', 'n'),
        #     ('data1',  100, 6.0,   40),
        #     ('data1',    2, 9.0, 3.3),
        #     ('data1', 3124, 3.0, 0.0000001),
        #     ('data2',  333, 6.0, 300909234),
        #     ('data2',   11, 2.0, 323432.2234),
        # ]


        transposed = [[r[i] for r in src] for i in range(len(src[0]))]
        # e.g.,
        # transposed = [
        #     ['component', 'data1', 'data1', 'data1', 'data2', 'data2'],
        #     ['v1', 100, 2, 3124, 333, 11],
        #     ['nvar', 6.0, 9.0, 3.0, 6.0, 2.0],
        #     ['n', 40, 3.3, 1e-07, 300909234, 323432.2234],
        #     ]

        transposed = [[int(e) if isinstance(e, float) and e.is_integer() else e for e in r] for r in transposed]
        transposed = [[str(e) for e in r] for r in transposed]

        columnWidths = [max([len(e) for e in r]) for r in transposed]
        # e.g., columnWidths = [9, 2, 4, 1]

        format = " {:>" + "s} {:>".join([str(e) for e in columnWidths]) + "s}"
        # e.g., format = "{:>9s} {:>4s} {:>4s} {:>11s}"

        ret = "\n".join([format.format(*row) for row in zip(*transposed)]) + "\n"
        # example ret
        # component   v1 nvar           n
        #     data1  100  6.0          40
        #     data1    2  9.0         3.3
        #     data1 3124  3.0       1e-07
        #     data2  333  6.0   300909234
        #     data2   11  2.0 323432.2234

        return ret

##__________________________________________________________________||
class WriteListToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def deliver(self, results):
        if results is None: return
        f = self._open(self._outPath)
        f.write(listToAlignedText(results))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
