#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.Counter import Counts
from AlphaTwirl.Binning import RoundLog

##__________________________________________________________________||
binning = RoundLog(0.1, 0)
counts = Counts()

vals = [float(v) for v in file('in.txt')]

for val in vals:
    bin = binning(val)
    counts.count(bin)

results = counts.results()
keys = results.keys()
keys.sort()
for k in  keys:
    row = (k, results[k]['n'], results[k]['nvar'])
    print "{:12.6f} {:6.0f} {:6.0f}".format(*row)

##__________________________________________________________________||
