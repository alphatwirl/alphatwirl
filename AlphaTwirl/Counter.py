# Tai Sakuma <sakuma@fnal.gov>
import pandas

import AlphaTwirl

##____________________________________________________________________________||
def buildBinningFromTbl(tbl_bin):
    return AlphaTwirl.Binning(bins = tbl_bin.bin.tolist(), lows = tbl_bin.low.tolist(), ups = tbl_bin.up.tolist())

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class Counter(object):
    def __init__(self, keyNames, keyComposer, countMethod, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethod = countMethod
        self._weightCalculator = weightCalculator

    def event(self, event):
        key = self._keyComposer(event)
        weight = self._weightCalculator(event)
        self._countMethod.count(key, weight)

    def keynames(self):
        return self._keynames

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class CounterBuilder(Counter):
    def __init__(self, keyNames, keyComposer, countMethodClass, weightCalculator = WeightCalculatorOne()):
        self._keynames = keyNames
        self._keyComposer = keyComposer
        self._countMethodClass = countMethodClass
        self._weightCalculator = weightCalculator

    def __call__(self):
        return Counter(self._keynames, self._keyComposer, self._countMethodClass(), self._weightCalculator)

##____________________________________________________________________________||
class keyComposer_alphaT(object):
    def __init__(self):
        tbl_bin = pandas.read_table("tbl/tbl_bin_alphaT.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

    def __call__(self, event):
        alphaT = event.alphaT
        alphaT_bin = self.binning(alphaT)
        return (alphaT_bin, )

##____________________________________________________________________________||
class keyComposer_met(object):
    def __init__(self):
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

    def __call__(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        return (met_bin, )

##____________________________________________________________________________||
class keyComposer_nvtx(object):
    def __call__(self, event):
        nVert = event.nVert
        return (nVert, )

##____________________________________________________________________________||
class keyComposer_met_nvtx(object):
    def __init__(self):
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

    def __call__(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        nVert = event.nVert
        return (met_bin, nVert)

##____________________________________________________________________________||
