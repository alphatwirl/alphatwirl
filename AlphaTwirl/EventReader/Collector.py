# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class Collector(object):
    def __init__(self, resultsCombinationMethod, deliveryMethod):
        self.resultsCombinationMethod = resultsCombinationMethod
        self.deliveryMethod = deliveryMethod

        self._datasetReaderPairs = [ ]

    def addReader(self, datasetName, reader):
        self._datasetReaderPairs.append((datasetName, reader))

    def collect(self):
        results = self.resultsCombinationMethod.combine(self._datasetReaderPairs)
        self.deliveryMethod.deliver(results)

##____________________________________________________________________________||
