# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class TreeReaderPackage(object):
    def __init__(self, CounterClass, collector):
        self._CounterClass = CounterClass
        self._collector = collector

    def make(self, datasetName):
        reader = self._CounterClass()
        self._collector.addReader(datasetName, reader)
        return reader

    def collect(self):
        self._collector.collect()

##____________________________________________________________________________||
