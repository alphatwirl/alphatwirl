# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from ..progressbar import ProgressReport

import alphatwirl

class DeprecatedOption(object): pass
DEPRECATEDOPTION = DeprecatedOption()

logger = logging.getLogger(__name__)

##__________________________________________________________________||
class CollectorComposite(object):

    """A composite of collectors.

    This class is a composite in the composite pattern.

    Examples of collectors are instances of `Collector`,
    `NullCollector`, and this class.

    """

    def __init__(self, progressReporter=DEPRECATEDOPTION):

        if progressReporter is not DEPRECATEDOPTION:
            text = '{}: the option "{}" is deprecated.'.format(
                self.__class__.__name__,
                'progressReporter'
            )
            logger.warning(text)

        self.components = [ ]
        self.progressReporter = progressReporter

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
            report = ProgressReport(name = 'collecting results', done = i + 1, total = len(self.components))
            alphatwirl.progressbar.report_progress(report)
            ret.append(collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
                                          for dataset, readerComposites in dataset_readers_list]))
        return ret

        ## in one line without the progress bar
        #return [collector.collect([(dataset, tuple(r.readers[i] for r in readerComposites))
        #                           for dataset, readerComposites in dataset_readers_list])
        #        for i, collector in enumerate(self.components)]

##__________________________________________________________________||
