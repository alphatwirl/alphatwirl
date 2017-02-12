# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport

##__________________________________________________________________||
class CollectorComposite(object):

    """A composite of collectors.

    This class is a composite in the composite pattern.

    Examples of collectors are instances of `Collector`,
    `NullCollector`, and this class.

    """

    def __init__(self, progressReporter = None):
        self.components = [ ]
        self.progressReporter = progressReporter

    def __repr__(self):
        return '{}(components = {!r}, progressReporter = {!r})'.format(
            self.__class__.__name__,
            self.components,
            self.progressReporter
        )

    def add(self, collector):
        """add a collector


        Args:
            collector: the collector to be added

        """
        self.components.append(collector)

    def addReader(self, datasetName, reader):
        readerComposite = reader
        for collector, reader in zip(self.components, readerComposite.readers):
            collector.addReader(datasetName, reader)

    def collect(self):
        """collect results


        Returns:
            a list of results

        """
        results = [ ]
        for i, collector in enumerate(self.components):
            if self.progressReporter is not None:
                report = ProgressReport(name = "collecting results", done = i + 1, total = len(self.components))
                self.progressReporter.report(report)
            results.append(collector.collect())
        return results

##__________________________________________________________________||
