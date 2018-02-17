# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class Parallel(object):
    def __init__(self, progressMonitor, communicationChannel, workingarea=None):
        self.progressMonitor = progressMonitor
        self.communicationChannel = communicationChannel
        self.workingarea = workingarea

    def __repr__(self):
        name_value_pairs = (
            ('progressMonitor',      self.progressMonitor),
            ('communicationChannel', self.communicationChannel),
            ('workingarea',          self.workingarea)

        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self):
        self.progressMonitor.begin()
        self.communicationChannel.begin()

    def terminate(self):
        self.communicationChannel.terminate()

    def end(self):
        self.progressMonitor.end()
        self.communicationChannel.end()

##__________________________________________________________________||
