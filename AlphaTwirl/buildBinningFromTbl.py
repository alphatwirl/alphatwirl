# Tai Sakuma <sakuma@fnal.gov>
import AlphaTwirl
import pandas

##____________________________________________________________________________||
def buildBinningFromTbl(path, retvalue = 'lowedge'):
    tbl = pandas.read_table(path, delim_whitespace=True)
    if retvalue == 'number':
        return AlphaTwirl.Binning.Binning(bins = tbl.bin.tolist(), lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)
    if retvalue == 'lowedge':
        return AlphaTwirl.Binning.Binning(lows = tbl.low.tolist(), ups = tbl.up.tolist(), retvalue = retvalue)

##____________________________________________________________________________||
