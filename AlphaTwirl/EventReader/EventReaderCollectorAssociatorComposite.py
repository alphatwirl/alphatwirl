# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport
from .EventReaderComposite import EventReaderComposite

##__________________________________________________________________||
class EventReaderCollectorAssociatorComposite(object):

    def __init__(self, progressReporter = None):
        self.associators = [ ]
        self.progressReporter = progressReporter

    def add(self, associator):
        self.associators.append(associator)

    def make(self, datasetName):
        readerComposite = EventReaderComposite()
        for associator in self.associators:
            reader = associator.make(datasetName)
            readerComposite.add(reader)
        return readerComposite

    def collect(self):
        for i, associator in enumerate(self.associators):
            if self.progressReporter is not None:
                report = ProgressReport(name = "collecting results", done = i + 1, total = len(self.associators))
                self.progressReporter.report(report)
            associator.collect()


##__________________________________________________________________||
