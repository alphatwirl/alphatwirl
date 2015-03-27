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
        try:
            return [self.__call__(v) for v in val]
        except TypeError:
            pass
        if not self._valid(val): return None
        return val

    def next(self, bin):
        try:
            return [self.next(v) for v in bin]
        except TypeError:
            pass
        return self._nextFunc(bin)

##____________________________________________________________________________||
