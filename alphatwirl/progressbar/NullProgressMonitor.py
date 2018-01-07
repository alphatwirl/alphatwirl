# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class NullProgressMonitor(object):
    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def createReporter(self): return None
    def begin(self): pass
    def end(self): pass

##__________________________________________________________________||
