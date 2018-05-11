# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.datasetloop import DatasetReaderComposite
from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.datasetloop.DatasetReaderComposite instead.')
class ComponentReaderComposite(DatasetReaderComposite):
    def __init__(self):
        super(ComponentReaderComposite, self).__init__()

##__________________________________________________________________||
