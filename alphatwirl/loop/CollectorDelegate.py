# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class CollectorDelegate(object):

    """
    """

    def __init__(self, collector):
        self.collector = collector

    def collect(self, dataset_reader_pairs):
        return self.collector.collect(dataset_reader_pairs)

##__________________________________________________________________||
