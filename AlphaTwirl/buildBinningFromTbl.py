# Tai Sakuma <sakuma@fnal.gov>
import Binning
import pandas

##____________________________________________________________________________||
def buildBinningFromTbl(path, retvalue = 'lowedge'):
    tbl = pandas.read_table(path, delim_whitespace=True)
    if retvalue == 'number':
        return Binning.Binning(bins = tbl.bin.tolist(), lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)
    if retvalue == 'lowedge':
        return Binning.Binning(lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)

##____________________________________________________________________________||
