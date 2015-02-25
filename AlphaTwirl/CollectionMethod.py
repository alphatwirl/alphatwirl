# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class CollectionMethod(object):
    def __init__(self, resultsCombinationMethod, deliveryMethod):
        self.resultsCombinationMethod = resultsCombinationMethod
        self.deliveryMethod = deliveryMethod

    def collect(self, datasetReaderPairs):
        results = self.resultsCombinationMethod.combine(datasetReaderPairs)
        self.deliveryMethod.deliver(results)

##____________________________________________________________________________||
