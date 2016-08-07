# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import NullProgressMonitor

##__________________________________________________________________||
class EventLoopRunner(object):
    """This class runs instances of `EventLoop`.

    """
    def __init__(self, progressMonitor = None):
        if progressMonitor is None: progressMonitor = NullProgressMonitor()
        self.progressReporter = progressMonitor.createReporter()

    def begin(self): pass

    def run(self, eventLoop):
        eventLoop(self.progressReporter)

    def end(self): pass

##__________________________________________________________________||
