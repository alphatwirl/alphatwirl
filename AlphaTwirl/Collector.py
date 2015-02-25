# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class Collector(object):
    def __init__(self, method):
        self._method = method
        self._datasetReaderPairs = [ ]

    def addReader(self, datasetName, reader):
        self._datasetReaderPairs.append((datasetName, reader))

    def collect(self):
        self._method.collect(self._datasetReaderPairs)

##____________________________________________________________________________||
