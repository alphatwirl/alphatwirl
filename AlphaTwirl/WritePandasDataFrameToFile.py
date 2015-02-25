# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class WritePandasDataFrameToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def deliver(self, results):
        f = open(self._outPath, 'w')
        results.to_string(f, index = False)
        f.close()

##____________________________________________________________________________||
