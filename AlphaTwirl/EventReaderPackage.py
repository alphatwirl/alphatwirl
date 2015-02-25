# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class EventReaderPackage(object):
    def __init__(self, ReaderClass, resultCollector):
        self._ReaderClass = ReaderClass
        self._resultCollector = resultCollector

    def make(self, datasetName):
        reader = self._ReaderClass()
        self._resultCollector.addReader(datasetName, reader)
        return reader

    def collect(self):
        self._resultCollector.collect()

##____________________________________________________________________________||
