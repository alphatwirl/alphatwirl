# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class EventReaderPackage(object):
    def __init__(self, ReaderClass, resultCollector = None):
        self._ReaderClass = ReaderClass
        self._resultCollector = resultCollector if resultCollector is not None else NullCollector()

    def make(self, datasetName):
        reader = self._ReaderClass()
        self._resultCollector.addReader(datasetName, reader)
        return reader

    def collect(self):
        self._resultCollector.collect()

##____________________________________________________________________________||
class NullCollector(object):
    def collect(self): pass
    def addReader(self, datasetName, reader): pass

##____________________________________________________________________________||
