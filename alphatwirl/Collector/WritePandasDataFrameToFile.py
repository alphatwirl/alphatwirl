# Tai Sakuma <tai.sakuma@cern.ch>
from ..misc import mkdir_p
import os

##__________________________________________________________________||
class WritePandasDataFrameToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def deliver(self, results):
        if results is None: return
        f = self._open(self._outPath)
        if len(results.index) == 0:
            f.write(" ".join([i for i in results.columns]) + "\n")
        else:
            results.to_string(f, index = False)
            f.write("\n")
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
