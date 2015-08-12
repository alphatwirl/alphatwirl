# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class CollectorDelegate(object):

    """
    """

    def __init__(self, collector):
        self.collector = collector

    def addReader(self, datasetName, reader):
        self.collector.addReader(datasetName, reader.reader)

    def collect(self):
        self.collector.collect()

##__________________________________________________________________||
