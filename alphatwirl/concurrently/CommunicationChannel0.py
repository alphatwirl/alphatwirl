# Tai Sakuma <tai.sakuma@cern.ch>
from ..progressbar import NullProgressMonitor

##__________________________________________________________________||
class CommunicationChannel0(object):
    """A communication channel for the single process mode

    An alternative to `CommunicationChannel`. However, unlike
    `CommunicationChannel`, this class does not send tasks to workers.
    Instead, it directly executes tasks.

    This class has the same interface as the class
    `CommunicationChannel`. When this class is used as a substitute
    for `CommunicationChannel`, the tasks will be sequentially
    executed in the foreground.

    """

    def __init__(self, progressMonitor = None):
        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor
        self.results = [ ]

    def begin(self):
        self.progressReporter = self.progressMonitor.createReporter()

    def put(self, task, *args, **kwargs):
        try:
            result = task(progressReporter = self.progressReporter, *args, **kwargs)
        except TypeError:
            result = task(*args, **kwargs)
        self.results.append(result)

    def receive(self):
        ret = self.results[:]
        del self.results[:]
        return ret

    def end(self): pass

##__________________________________________________________________||
