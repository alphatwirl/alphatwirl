# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return None
    def begin(self): pass
    def end(self): pass

##____________________________________________________________________________||
