# Tai Sakuma <tai.sakuma@gmail.com>

from .ReturnTrue import ReturnTrue

##__________________________________________________________________||
class PlusOne(object):
    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def __call__(self, x):
        return x + 1

##__________________________________________________________________||
class Echo(object):
    def __init__(self, nextFunc=PlusOne(), valid=ReturnTrue()):
        self._nextFunc = nextFunc
        self._valid = valid

    def __repr__(self):
        return '{}(nextFunc={!r}, valid={!r})'.format(
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
