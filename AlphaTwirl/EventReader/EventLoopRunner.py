# Tai Sakuma <sakuma@fnal.gov>
from NullProgressMonitor import NullProgressMonitor

##____________________________________________________________________________||
class EventLoopRunner(object):
    def __init__(self, progressMonitor = None):
        if progressMonitor is None: progressMonitor = NullProgressMonitor()
        self.progressReporter = progressMonitor.createReporter()

    def begin(self): pass

    def run(self, eventLoop):
        eventLoop(self.progressReporter)

    def end(self): pass

##____________________________________________________________________________||
