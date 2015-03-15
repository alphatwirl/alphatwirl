# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class NullProgressReporter(object):
    def report(self, report): pass

##____________________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return NullProgressReporter()
    def addWorker(self, worker): pass
    def monitor(self): pass
    def last(self): pass

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
