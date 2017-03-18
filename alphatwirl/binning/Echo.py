# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
def plusOne(x): return x + 1

##__________________________________________________________________||
class Echo(object):
    def __init__(self, nextFunc = plusOne, valid = returnTrue):
        self._nextFunc = nextFunc
        self._valid = valid

    def __repr__(self):
        return '{}(nextFunc = {!r}, valid = {!r})'.format(
            self.__class__.__name__,
            self._nextFunc,
            self._valid
        )

    def __call__(self, val):
        if not self._valid(val): return None
        return val

    def next(self, bin):
        if self._nextFunc is None: return None
        return self._nextFunc(bin)

##__________________________________________________________________||
