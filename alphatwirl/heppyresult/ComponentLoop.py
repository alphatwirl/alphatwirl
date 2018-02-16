# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, heppyResult, reader):
        self.reader = reader
        self.heppyResult = heppyResult
        self.components = self.heppyResult.components()
        self.datasetloop = DatasetLoop(datasets=self.components, reader=self.reader)

    def __repr__(self):
        name_value_pairs = (
            ('reader',      self.reader),
            ('heppyResult', self.heppyResult),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        return self.datasetloop()

##__________________________________________________________________||
class DatasetLoop(object):

    def __init__(self, datasets, reader):
        self.datasets = datasets
        self.reader = reader

    def __call__(self):
        self.reader.begin()
        for dataset in self.datasets:
            self.reader.read(dataset)
        return self.reader.end()

##__________________________________________________________________||
