# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class CollectorDelegate(object):

    """
    """

    def __init__(self, collector):
        self.collector = collector

    def __repr__(self):
        name_value_pairs = (
            ('collector', self.collector),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def collect(self, dataset_readers_list):
        return self.collector.collect(dataset_readers_list)

##__________________________________________________________________||
