# Tai Sakuma <tai.sakuma@cern.ch>
from ..progressbar import ProgressReport

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
        name_value_pairs = (
            ('components',       self.components),
            ('progressReporter', self.progressReporter),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def add(self, collector):
        """add a collector


        Args:
            collector: the collector to be added

        """
        self.components.append(collector)

    def collect(self, dataset_readers_list):
        """collect results


        Returns:
            a list of results

        """

        ret = [ ]
        for i, collector in enumerate(self.components):
            if self.progressReporter is not None:
                report = ProgressReport(name = 'collecting results', done = i + 1, total = len(self.components))
                self.progressReporter.report(report)
            ret.append(collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
                                          for dataset, readerComposites in dataset_readers_list]))
        return ret

        ## in one line without the progress bar
        #return [collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
        #                           for dataset, readerComposites in dataset_readers_list])
        #        for i, collector in enumerate(self.components)]

##__________________________________________________________________||
