# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class Collector(object):

    """This class collects results, i.e., this class combines results
    of readers and deliver them.

    Methods for combination and delivery are specified at the
    instantiation.

    Readers are typically instances of the same class initialized in
    the same way. Each reader reads a data set. A pair of the name of
    a data set and the reader that reads the data set is given to this
    class via the method ``addReader``.

    The method ``collect`` is called after the event loop. It returns
    the combined results.

    """

    def __init__(self, resultsCombinationMethod, deliveryMethod = None):
        self.resultsCombinationMethod = resultsCombinationMethod
        self.deliveryMethod = deliveryMethod if deliveryMethod is not None else NullDeliveryMethod()

        self._datasetReaderPairs = [ ]

    def __repr__(self):
        return '{}(resultsCombinationMethod = {!r}, deliveryMethod = {!r}, datasetReaderPairs = {!r})'.format(
            self.__class__.__name__,
            self.resultsCombinationMethod,
            self.deliveryMethod,
            self._datasetReaderPairs
        )

    def addReader(self, datasetName, reader):
        self._datasetReaderPairs.append((datasetName, reader))

    def collect(self):
        results = self.resultsCombinationMethod.combine(self._datasetReaderPairs)
        self.deliveryMethod.deliver(results)
        return results

##__________________________________________________________________||
class NullDeliveryMethod(object):
    def deliver(self, results): pass

##__________________________________________________________________||
