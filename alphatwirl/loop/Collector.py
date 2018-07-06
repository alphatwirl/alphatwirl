# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class Collector(object):

    """This class collects results, i.e., this class combines results
    of readers and deliver them.

    Methods for combination and delivery are specified at the
    instantiation.

    Readers are typically instances of the same class initialized in
    the same way. Each reader reads a data set..

    The method ``collect`` is called with a list of pairs of a data
    set and a reader after the event loop. It returns the combined
    results.

    """

    def __init__(self, resultsCombinationMethod, deliveryMethod = None):
        self.resultsCombinationMethod = resultsCombinationMethod
        self.deliveryMethod = deliveryMethod if deliveryMethod is not None else NullDeliveryMethod()

        self._repr_pairs = [
            ('resultsCombinationMethod', self.resultsCombinationMethod),
            ('deliveryMethod',           self.deliveryMethod),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def __str__(self):
        nwidth = max(len(n) for n, _ in self._repr_pairs)
        nwidth += 4
        return '{}:\n{}'.format(
            self.__class__.__name__,
            '\n'.join(['{:>{}}: {!r}'.format(n, nwidth, v) for n, v in self._repr_pairs]),
        )

    def collect(self, dataset_readers_list):
        results = self.resultsCombinationMethod.combine(dataset_readers_list)
        self.deliveryMethod.deliver(results)
        return results

##__________________________________________________________________||
class NullDeliveryMethod(object):
    def deliver(self, results): pass

##__________________________________________________________________||
