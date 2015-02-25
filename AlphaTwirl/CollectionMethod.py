# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class CollectionMethod(object):
    def __init__(self, resultsCombinationMethod, deliveryMethod):
        self.resultsCombinationMethod = resultsCombinationMethod
        self.deliveryMethod = deliveryMethod

    def collect(self, rpairs):
        results = self.resultsCombinationMethod.combine(rpairs)
        self.deliveryMethod.deliver(results)

##____________________________________________________________________________||
