# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class EventReaderCollectorAssociator(object):

    """This class associates event readers and a result collector.

    An instance of this class is initialized with a reader class and a
    collector.

    An example of a reader class is `Counter`. The class itself rather
    than its instance needs to be given. Alternatively, an instance of
    a factory of instances of the reader class can be given as well.
    For example, instead of the class `Counter`, an instance of its
    factory class `CounterFactory` can be given as well.

    An example of a collector is `Collector`. Unlike the reader class
    mentioned above, an instance of `Collector` not the class itself
    should be given.

    When the method `make()` is called with a data set name, this
    class creates a reader, provide the collector with the pair of the
    data set name and the reader, and returns the reader.

    """

    def __init__(self, ReaderClass, resultCollector = None):
        self._ReaderClass = ReaderClass
        self.collector = resultCollector if resultCollector is not None else NullCollector()

    def make(self, datasetName):
        """make a reader and associates it with the collector.


        Args:
            datasetName (str): the name of the data set that the reader will read

        Returns:
            the reader that is made

        """
        reader = self._ReaderClass()
        self.collector.addReader(datasetName, reader)
        return reader

##____________________________________________________________________________||
class NullCollector(object):
    def collect(self): return None
    def addReader(self, datasetName, reader): pass

##____________________________________________________________________________||
