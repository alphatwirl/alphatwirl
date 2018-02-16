# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class DatasetLoop(object):

    def __init__(self, datasets, reader):
        self.datasets = datasets
        self.reader = reader

    def __repr__(self):
        name_value_pairs = (
            ('datasets', self.datasets),
            ('reader', self.reader),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        self.reader.begin()
        for dataset in self.datasets:
            self.reader.read(dataset)
        return self.reader.end()

##__________________________________________________________________||
