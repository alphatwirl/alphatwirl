# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
def returnTrue(x): return True

##____________________________________________________________________________||
def plusOne(x): return x + 1

##____________________________________________________________________________||
class Echo(object):
    def __init__(self, nextFunc = plusOne, valid = returnTrue):
        self._nextFunc = nextFunc
        self._valid = valid

    def __call__(self, val):
        if not self._valid(val): return None
        return val

    def next(self, bin):
        if self._nextFunc is None: return None
        return self._nextFunc(bin)

##____________________________________________________________________________||
