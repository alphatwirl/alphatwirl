# Tai Sakuma <sakuma@fnal.gov>
import pandas

import AlphaTwirl

##____________________________________________________________________________||
def buildBinningFromTbl(tbl_bin):
    return AlphaTwirl.Binning(bins = tbl_bin.bin.tolist(), lows = tbl_bin.low.tolist(), ups = tbl_bin.up.tolist())

##____________________________________________________________________________||
class CounterBase(object):
    def __init__(self):
        self.counts = AlphaTwirl.Counts()

    def _count(self, key, weight):
        self.counts.count(key, weight)

    def keynames(self):
        return self._keynames

    def results(self):
        return self.counts.counts

##____________________________________________________________________________||
class Counter_alphaT(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        tbl_bin = pandas.read_table("tbl/tbl_bin_alphaT.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('alphaT_bin', )

    def event(self, event):
        alphaT = event.alphaT
        alphaT_bin = self.binning(alphaT)
        key = (alphaT_bin, )
        self._count(key, 1.0)


##____________________________________________________________________________||
class Counter_met(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('met_bin', )

    def event(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        key = (met_bin, )
        self._count(key, 1.0)

##____________________________________________________________________________||
class Counter_nvtx(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)

        self._keynames = ('nvtx', )

    def event(self, event):
        nVert = event.nVert
        key = (nVert, )
        self._count(key, 1.0)

##____________________________________________________________________________||
class Counter_met_nvtx(CounterBase):
    def __init__(self):
        CounterBase.__init__(self)
        tbl_bin = pandas.read_table("tbl/tbl_bin.txt", delim_whitespace=True)
        self.binning = buildBinningFromTbl(tbl_bin)

        self._keynames = ('met_bin', 'nvtx', )

    def event(self, event):
        met_pt = event.met_pt
        met_bin = self.binning(met_pt)
        nVert = event.nVert
        key = (met_bin, nVert)
        self._count(key, 1.0)

##____________________________________________________________________________||
