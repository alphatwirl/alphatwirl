# Tai Sakuma <sakuma@fnal.gov>
import AlphaTwirl
import pandas

##____________________________________________________________________________||
def buildBinningFromTbl(path):
    tbl = pandas.read_table(path, delim_whitespace=True)
    return AlphaTwirl.Binning.Binning(bins = tbl.bin.tolist(), lows = tbl.low.tolist(), ups = tbl.up.tolist())

##____________________________________________________________________________||
