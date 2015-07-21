# Tai Sakuma <tai.sakuma@cern.ch>
from Round import Round
import math

##____________________________________________________________________________||
def returnTrue(x): return True

##____________________________________________________________________________||
class RoundLog(object):
    def __init__(self, width = 0.1, aBoundary = 1, retvalue = 'lowedge', valid = returnTrue):
        self._round = Round(width = width, aBoundary = math.log10(aBoundary), retvalue = retvalue)
        self.valid = valid

    def __call__(self, val):
        if not self.valid(val): return None
        if val <= 0: return None
        val = math.log10(val)
        return 10**self._round(val)

    def next(self, bin):
        bin = math.log10(bin)
        return 10**self._round.next(bin)

##____________________________________________________________________________||
