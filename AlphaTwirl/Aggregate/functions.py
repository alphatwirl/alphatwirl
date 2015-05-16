# Tai Sakuma <tai.sakuma@cern.ch>
import pandas as pd


##____________________________________________________________________________||
def sumOverCategories(tbl, categories, variables):

    if categories is None: categories = ()
    factor_names = [c for c in tbl.columns if c not in categories + variables]

    if len(factor_names) == 0:

        # group by dummy index [1, 1, ...]
        tbl = tbl.groupby([1]*len(tbl.index))[variables].sum().reset_index()

        # remove the column added by groupby, which is 'index' unless
        # 'index' already exists
        tbl = tbl.drop([c for c in tbl.columns if c not in variables], axis = 1)
        return tbl

    tbl = tbl.groupby(factor_names)[variables].sum().reset_index()
    return tbl

##____________________________________________________________________________||
def normalizeToXsec(tbl, tbl_process, tbl_nevt, tbl_xsec):

    tbl_xsec = pd.merge(tbl_process, tbl_xsec)
    tbl_xsec = tbl_xsec[['phasespace', 'xsec']].drop_duplicates()

    tbl = pd.merge(tbl_process, tbl)
    tbl = sumOverCategories(tbl, categories = ('component', ), variables = ('n', 'nvar'))

    tbl_nevt = tbl_nevt.drop('nevt_sumw', axis = 1)
    tbl_nevt = pd.merge(tbl_process, tbl_nevt)
    tbl_nevt = sumOverCategories(tbl_nevt, categories = ('component', ), variables = ('nevt', ))
    tbl_nevt = pd.merge(tbl_nevt, tbl_xsec)

    tbl = pd.merge(tbl, tbl_nevt)
    lumi = 4000
    tbl.n = tbl.n*tbl.xsec/tbl.nevt*lumi
    tbl.nvar = tbl.nvar*(tbl.xsec/tbl.nevt*lumi)**2
    del tbl['nevt']
    del tbl['xsec']

    tbl = sumOverCategories(tbl, categories = ('phasespace', ), variables = ('n', 'nvar'))

    return tbl

##____________________________________________________________________________||
