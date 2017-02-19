# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import NullProgressMonitor

##__________________________________________________________________||
class EventLoopRunner(object):
    """This class runs instances of `EventLoop` and keeps the results. It
    will return the results when `end()` is called.

    """
    def __init__(self, progressMonitor = None):
        if progressMonitor is None: progressMonitor = NullProgressMonitor()
        self.progressReporter = progressMonitor.createReporter()
        self.results = [ ]

    def begin(self):
        self.results = [ ]

    def run(self, eventLoop):
        self.results.append(eventLoop(self.progressReporter))

    def end(self):
        return self.results

##__________________________________________________________________||
