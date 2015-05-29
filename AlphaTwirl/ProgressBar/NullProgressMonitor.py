# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return None
    def addWorker(self, worker): pass
    def monitor(self): pass
    def last(self): pass

##____________________________________________________________________________||
