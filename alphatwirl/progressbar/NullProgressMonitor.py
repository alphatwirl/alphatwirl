# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return None
    def begin(self): pass
    def end(self): pass

##__________________________________________________________________||
