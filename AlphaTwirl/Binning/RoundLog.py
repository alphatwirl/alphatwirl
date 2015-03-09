# Tai Sakuma <sakuma@fnal.gov>
from Round import Round
import math

##____________________________________________________________________________||
class RoundLog(object):
    def __init__(self, width = 0.1, aBoundary = 0, retvalue = 'center'):
        self._round = Round(width = width, aBoundary = aBoundary, retvalue = retvalue)

    def __call__(self, val):
        try:
            return [self.__call__(v) for v in val]
        except TypeError:
            pass
        val = math.log10(val)
        return 10**self._round(val)

    def next(self, bin):
        try:
            return [self.next(v) for v in bin]
        except TypeError:
            pass
        bin = math.log10(bin)
        return 10**self._round.next(bin)

##____________________________________________________________________________||
