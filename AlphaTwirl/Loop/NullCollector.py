# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class NullCollector(object):
    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def addReader(self, datasetName, reader):
        pass

    def collect(self):
        pass

##__________________________________________________________________||
