# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class WritePandasDataFrameToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def deliver(self, results):
        f = self._open(self._outPath)
        if len(results.index) == 0:
            f.write(" ".join([i for i in results.columns]) + "\n")
        else:
            results.to_string(f, index = False)
        self._close(f)

    def _open(self, path): return open(path, 'w')
    def _close(self, file): file.close()

##____________________________________________________________________________||
