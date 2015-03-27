# Tai Sakuma <tai.sakuma@cern.ch>

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
