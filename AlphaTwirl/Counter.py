# Tai Sakuma <sakuma@fnal.gov>
import pandas

import AlphaTwirl

##____________________________________________________________________________||
def buildBinningFromTbl(tbl_bin):
    return AlphaTwirl.Binning(bins = tbl_bin.bin.tolist(), lows = tbl_bin.low.tolist(), ups = tbl_bin.up.tolist())

##____________________________________________________________________________||
class CounterBase(object):
    def __init__(self):
        pass

    def event(self, event):
        key = self._keyComposer(event)
        weight = self._weightCalculator(event)
        self._countMethod.count(key, weight)

    def keynames(self):
        return self._keynames

    def results(self):
        return self._countMethod.results()

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##____________________________________________________________________________||
class Counter_alphaT(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        self._countMethod = AlphaTwirl.Counts()
        tbl_bin = pandas.read_table("tbl/tbl_bin_alphaT.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('alphaT_bin', )

        self._weightCalculator = WeightCalculatorOne()

    def _keyComposer(self, event):
        alphaT = event.alphaT
        alphaT_bin = self.binning(alphaT)
        return (alphaT_bin, )

##____________________________________________________________________________||
class Counter_met(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        self._countMethod = AlphaTwirl.Counts()
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('met_bin', )

        self._weightCalculator = WeightCalculatorOne()

    def _keyComposer(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        return (met_bin, )

##____________________________________________________________________________||
class Counter_nvtx(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        self._countMethod = AlphaTwirl.Counts()

        self._keynames = ('nvtx', )

        self._weightCalculator = WeightCalculatorOne()

    def _keyComposer(self, event):
        nVert = event.nVert
        return (nVert, )

##____________________________________________________________________________||
class Counter_met_nvtx(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        self._countMethod = AlphaTwirl.Counts()
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('met_bin', 'nvtx', )

        self._weightCalculator = WeightCalculatorOne()

    def _keyComposer(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        nVert = event.nVert
        return (met_bin, nVert)

##____________________________________________________________________________||
