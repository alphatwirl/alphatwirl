# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport
from .ReaderComposite import ReaderComposite
from .CollectorComposite import CollectorComposite

##__________________________________________________________________||
class EventReaderCollectorAssociatorComposite(object):

    """A composite of `EventReaderCollectorAssociator`.

    This class is a composite in the composite pattern.

    Attributes:
      collector (CollectorComposite): a composite of collectors
      components: a list of the associators, the components of the composite

    """

    def __init__(self, progressReporter = None):
        self.collector = CollectorComposite(progressReporter)
        self.components = [ ]

    def add(self, associator):
        """add an associator.


        Args:
            associator: the associator to be added

        """
        self.components.append(associator)
        self.collector.add(associator.collector)

    def make(self, datasetName):
        """make an `ReaderComposite`.


        Args:
            datasetName (str): the name of the data set that the components of the `ReaderComposite` will read

        Returns:
            an instance of `ReaderComposite`

        """

        readerComposite = ReaderComposite()
        for associator in self.components:
            reader = associator.make(datasetName)
            readerComposite.add(reader)
        return readerComposite

##__________________________________________________________________||
