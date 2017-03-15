#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import pandas as pd

##__________________________________________________________________||
d1 = pd.read_table('tbl_process.txt', delim_whitespace = True)
d2 = pd.read_table('tbl_n_component.met.txt', delim_whitespace = True)
d3 = pd.read_table('tbl_nevt.txt', delim_whitespace = True)
d4 = pd.read_table('tbl_xsec.txt', delim_whitespace = True)

d = pd.merge(d1, d2)
d = d.groupby(['phasespace', 'process', 'met']).sum().reset_index()
e = pd.merge(d1, d3)
e = e.groupby(['phasespace', 'process']).sum().reset_index()
e = pd.merge(e, d4)
d = pd.merge(d, e)
lumi = 4000
d.n = d.n*d.xsec/d.nevt*lumi
d.nvar = d.nvar*(d.xsec/d.nevt*lumi)**2
del d['nevt']
del d['xsec']
d = d.groupby(['process', 'met']).sum().reset_index()

f = open('tbl_out_python.txt', 'w')
d.to_string(f, index = False)
f.write("\n")
f.close()

##__________________________________________________________________||
