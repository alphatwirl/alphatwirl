# Tai Sakuma <tai.sakuma@cern.ch>
import copy

##__________________________________________________________________||
class Associator(object):

    """This class associates event readers and a result collector.

    An instance of this class is initialized with a reader and a
    collector.

    An example of a reader is an instance of `Summarizer`.

    An example of a collector is `Collector`.

    When the method `make()` is called with a data set name, this
    class makes a copy of the reader, provide the collector with the
    pair of the data set name and the copy, and returns the the copy.

    """

    def __init__(self, reader, resultCollector = None):
        self.reader = reader
        self.collector = resultCollector if resultCollector is not None else NullCollector()

    def make(self, datasetName):
        """make a copy of the reader and associates it with the collector.


        Args:
            datasetName (str): the name of the data set that the reader will read

        Returns:
            the reader that is made

        """
        reader = copy.deepcopy(self.reader)
        self.collector.addReader(datasetName, reader)
        return reader

##__________________________________________________________________||
class NullCollector(object):
    def collect(self): return None
    def addReader(self, datasetName, reader): pass

##__________________________________________________________________||
