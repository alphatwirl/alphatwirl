# Tai Sakuma <tai.sakuma@gmail.com>
import logging

##__________________________________________________________________||
class Parallel(object):
    def __init__(self, progressMonitor=None, communicationChannel=None, workingarea=None):
        self.communicationChannel = communicationChannel
        self.workingarea = workingarea

        if progressMonitor is not None:
            # Not using @_deprecated_class_method_option() because
            # progressMonitor is usually given as a position argument
            # rather than a keyword argument.
            logger = logging.getLogger(__name__)
            logger.warning('progressMonitor is given. This is deprecated and will be ignored.')


    def __repr__(self):
        name_value_pairs = (
            ('communicationChannel', self.communicationChannel),
            ('workingarea',          self.workingarea)

        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self):
        self.communicationChannel.begin()

    def terminate(self):
        self.communicationChannel.terminate()

    def end(self):
        self.communicationChannel.end()

##__________________________________________________________________||
