# Tai Sakuma <tai.sakuma@gmail.com>
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
            towrite = " ".join([i for i in results.columns]) + "\n"
            towrite = towrite.encode()
            f.write(towrite)
        else:
            ## results.to_string(f, index = False)
            towrite = results.to_string(index = False) + "\n"
            towrite = towrite.encode()
            f.write(towrite)
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
