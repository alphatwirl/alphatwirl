# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, heppyResult, reader):
        self.reader = reader
        self.heppyResult = heppyResult

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
        self.reader.begin()
        for component in self.heppyResult.components():
            self.reader.read(component)
        return self.reader.end()

##__________________________________________________________________||
