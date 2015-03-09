# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class Echo(object):
    def __init__(self, nextFunc = lambda x: x + 1):
        self._nextFunc = nextFunc

    def __call__(self, val):
        try:
            return [self.__call__(v) for v in val]
        except TypeError:
            pass
        return val

    def next(self, bin):
        try:
            return [self.next(v) for v in bin]
        except TypeError:
            pass
        return self._nextFunc(bin)

##____________________________________________________________________________||
