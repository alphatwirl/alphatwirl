# Tai Sakuma <tai.sakuma@gmail.com>
import os
import gzip

try:
   import cPickle as pickle
except:
   import pickle

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
class ResumableDatasetLoop(object):

    def __init__(self, datasets, reader, workingarea):
        self.datasets = datasets
        self.reader = reader
        self.workingarea = workingarea

    def __repr__(self):
        name_value_pairs = (
            ('datasets', self.datasets),
            ('reader', self.reader),
            ('workingarea', self.workingarea),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        self.reader.begin()
        for dataset in self.datasets:
            self.reader.read(dataset)

        path = os.path.join(self.workingarea.path, 'reader.p.gz')
        with gzip.open(path, 'wb') as f:
            pickle.dump(self.reader, f, protocol=pickle.HIGHEST_PROTOCOL)

        return self.reader.end()

##__________________________________________________________________||
