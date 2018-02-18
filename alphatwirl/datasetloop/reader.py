# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class DatasetReaderComposite(object):

    def __init__(self):
        self.readers = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('readers', self.readers),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def add(self, reader):
        self.readers.append(reader)

    def begin(self):
        for reader in self.readers:
            reader.begin()

    def read(self, dataset):
        for reader in self.readers:
            reader.read(dataset)

    def end(self):
        return [reader.end() for reader in self.readers]

##__________________________________________________________________||
