# Tai Sakuma <tai.sakuma@gmail.com>

from alphatwirl.datasetloop import DatasetLoop
from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.datasetloop.DatasetLoop instead.')
class ComponentLoop(object):

    def __init__(self, heppyResult, reader):
        self.datasetloop = DatasetLoop(
            datasets=heppyResult.components(),
            reader=reader
        )
        self.name_value_pairs = (
            ('reader',      reader),
            ('heppyResult', heppyResult),
        )

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self.name_value_pairs]),
        )

    def __call__(self):
        return self.datasetloop()

##__________________________________________________________________||
