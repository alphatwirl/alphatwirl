# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from ..progressbar import ProgressReport

from alphatwirl.misc.deprecation import _deprecated_class_method_option

import alphatwirl


##__________________________________________________________________||
class CollectorComposite(object):

    """A composite of collectors.

    This class is a composite in the composite pattern.

    Examples of collectors are instances of `Collector`,
    `NullCollector`, and this class.

    """

    @_deprecated_class_method_option('progressReporter')
    def __init__(self, progressReporter=None):

        self.components = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('components',       self.components),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
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
            report = ProgressReport(name='collecting results', done=(i + 1), total=len(self.components))
            alphatwirl.progressbar.report_progress(report)
            ret.append(collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
                                          for dataset, readerComposites in dataset_readers_list]))
        return ret

        ## in one line without the progress bar
        #return [collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
        #                           for dataset, readerComposites in dataset_readers_list])
        #        for i, collector in enumerate(self.components)]

##__________________________________________________________________||
