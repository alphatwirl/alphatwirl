# Tai Sakuma <tai.sakuma@cern.ch>
import pandas as pd

##__________________________________________________________________||
def sumOverCategories(tbl, categories, variables):
    import logging
    logging.warning('the function "{}" is renamed "{}"'.format(
        "sumOverCategories", "sum_over_categories")
    )
    return sum_over_categories(tbl, categories, variables)

##__________________________________________________________________||
def sum_over_categories(tbl, categories, variables):

    if categories is None: categories = ()

    variables = tuple([v for v in variables if v in tbl.columns.values])

    factor_names = [c for c in tbl.columns if c not in categories + variables]

    if len(factor_names) == 0:

        # group by dummy index [1, 1, ...]
        tbl = tbl.groupby([1]*len(tbl.index))[variables].sum().reset_index()

        # remove the column added by groupby, which is 'index' unless
        # 'index' already exists
        tbl = tbl.drop([c for c in tbl.columns if c not in variables], axis = 1)
        return tbl

    ret = tbl.groupby(factor_names)[variables].sum().reset_index().dropna()

    ret = ret.reset_index(drop = True)

    ret = keep_dtype(ret, tbl)

    return ret

##__________________________________________________________________||
def combine_MC_yields_in_datasets_into_xsec_in_processes(
        tbl_yield, tbl_process, tbl_nevt, tbl_xsec, use_nevt_sumw = False):
    """return a data frame for cross sections for each process.

    This function receives four data frames:


    tbl_yield is the data frame for binned MC counts for each
    component (data set), e.g.,::

                  component            met     n  nvar
           QCD_HT_1000ToInf  15.8489319246     1     1
           QCD_HT_1000ToInf  19.9526231497     0     0
           QCD_HT_1000ToInf  25.1188643151     1     1
           QCD_HT_1000ToInf  31.6227766017     3     3
           QCD_HT_1000ToInf  39.8107170553     2     2
           QCD_HT_1000ToInf  50.1187233627     5     5
           QCD_HT_1000ToInf   63.095734448     2     2
           QCD_HT_1000ToInf  79.4328234724     2     2
           QCD_HT_1000ToInf            100     3     3
           QCD_HT_1000ToInf  125.892541179     2     2
           QCD_HT_1000ToInf  158.489319246     0     0
      QCD_HT_1000ToInf_ext1  39.8107170553     1     1
      QCD_HT_1000ToInf_ext1  50.1187233627     1     1


    The column 'component' is the data set. (The data set is called
    'component' in Heppy.)

    The column 'met' in this example are the bins. In this example,
    the bins are only one dimension. However, the bins can be
    multidimensional as well, in which case, the data frame will have
    multiple columns for the bins, e.g., met, njet, nbjet.

    Note that, the column names for the bins should not conflict with
    column names of any of the data frames in the argument. For
    example, 'xsec' or 'nevt' cannot be used for the column names for
    the bins (this restriction will be removed in the future).

    The column 'n' shows the counts in the bin in the component. The
    counts can be either raw or weighted.

    The column 'nvar' shows the errors on the counts in the bin in the
    component. When the 'n' is a raw count, the 'nvar' will typically
    have the same value as the 'n'.

    tbl_process is the data frame that relates the components, the
    phase spaces, and the processes, e.g.,::

                  component             phasespace  process
            QCD_HT_100To250        QCD_HT_100To250  QCD
            QCD_HT_250To500        QCD_HT_250To500  QCD
           QCD_HT_500To1000       QCD_HT_500To1000  QCD
           QCD_HT_1000ToInf       QCD_HT_1000ToInf  QCD
       QCD_HT_250To500_ext1        QCD_HT_250To500  QCD
      QCD_HT_500To1000_ext1       QCD_HT_500To1000  QCD
      QCD_HT_1000ToInf_ext1       QCD_HT_1000ToInf  QCD
             TToLeptons_sch         TToLeptons_sch  T
          TBarToLeptons_sch      TBarToLeptons_sch  T
             TToLeptons_tch         TToLeptons_tch  T
          TBarToLeptons_tch      TBarToLeptons_tch  T
                     T_tWch                 T_tWch  T
                  TBar_tWch              TBar_tWch  T
                     TTJets                 TTJets  TTJets
      WJetsToLNu_HT100to200  WJetsToLNu_HT100to200  WJetsToLNu
      WJetsToLNu_HT200to400  WJetsToLNu_HT200to400  WJetsToLNu
      WJetsToLNu_HT400to600  WJetsToLNu_HT400to600  WJetsToLNu
      WJetsToLNu_HT600toInf  WJetsToLNu_HT600toInf  WJetsToLNu

    tbl_nevt is the data frame that shows the number of the generated
    events for each component, e.g.,::

                  component     nevt     nevt_sumw
           QCD_HT_1000ToInf  1130720       1130720
      QCD_HT_1000ToInf_ext1   333733        333733
            QCD_HT_100To250  4123612       4123612
            QCD_HT_250To500  2004219       2004219
       QCD_HT_250To500_ext1   663953        663953
           QCD_HT_500To1000  3214312       3214312
      QCD_HT_500To1000_ext1   849033        849033
                     T_tWch   986100        986100
                  TBar_tWch   971800        971800
          TBarToLeptons_sch   250000 320855.887262
          TBarToLeptons_tch  1999800 50734279.1235
                     TTJets 25446993      25446993
             TToLeptons_sch   500000 1042218.60703
             TToLeptons_tch  3991000 173500373.328
      WJetsToLNu_HT100to200  5262265       5262265
      WJetsToLNu_HT200to400  4936077       4936077
      WJetsToLNu_HT400to600  4640594       4640594
      WJetsToLNu_HT600toInf  4581841       4581841

    tbl_xsec shows the cross sections of each component, e.g.,::

                  component     xsec
           QCD_HT_1000ToInf    769.7
      QCD_HT_1000ToInf_ext1    769.7
            QCD_HT_100To250 28730000
            QCD_HT_250To500   670500
       QCD_HT_250To500_ext1   670500
           QCD_HT_500To1000    26740
      QCD_HT_500To1000_ext1    26740
                     T_tWch     35.6
                  TBar_tWch     35.6
          TBarToLeptons_sch  1.34784
          TBarToLeptons_tch 26.23428
                     TTJets    809.1
             TToLeptons_sch   2.3328
             TToLeptons_tch  44.0802
      WJetsToLNu_HT100to200  2234.91
      WJetsToLNu_HT200to400  580.068
      WJetsToLNu_HT400to600  68.4003
      WJetsToLNu_HT600toInf  23.1363

    All components in the same phase space need to have the same cross
    section. In the example above, QCD_HT_1000ToInf and
    QCD_HT_1000ToInf_ext1 are two components in the same phase space
    and have the same cross section, 769.7.

    return value

    The function returns the data frame for the cross sections in the
    same bins by processes.::

     process          met      xsec       xsecvar
         QCD    15.848932  0.013687  8.688971e-05
         QCD    19.952623  0.052646  3.464539e-04
         QCD    25.118864  0.264983  6.323639e-02
         QCD    31.622777  0.266034  6.323694e-02
         QCD    39.810717  0.034481  2.173624e-04
         QCD    50.118723  0.300515  6.345431e-02
         QCD    63.095734  0.053697  3.470063e-04
         QCD    79.432823  0.265508  6.323667e-02
         QCD   100.000000  0.015264  8.771844e-05
         QCD   125.892541  0.014213  8.716595e-05
         QCD   158.489319  0.006581  4.330673e-05
         QCD   199.526231  0.000000  0.000000e+00
           T     1.584893  0.000073  2.645322e-09
           T     1.995262  0.000109  3.987302e-09
           T     2.511886  0.000445  1.499073e-08
           T     3.162278  0.000571  1.545752e-08
           T     3.981072  0.001429  3.620408e-08

    The unit of 'xsec' will be the same as in tbx_xsec. In this
    example, it is pb.

    """

    tbl_xsec = pd.merge(tbl_process, tbl_xsec)
    tbl_xsec = tbl_xsec[['phasespace', 'xsec']].drop_duplicates()

    tbl = pd.merge(tbl_process, tbl_yield)
    tbl = sum_over_categories(tbl, categories = ('component', ), variables = ('n', 'nvar'))

    if use_nevt_sumw:
        tbl_nevt = tbl_nevt.drop('nevt', axis = 1)
        tbl_nevt = pd.merge(tbl_process, tbl_nevt)
        tbl_nevt = sum_over_categories(tbl_nevt, categories = ('component', ), variables = ('nevt_sumw', ))
        tbl_nevt = pd.merge(tbl_nevt, tbl_xsec)
    else:
        tbl_nevt = tbl_nevt.drop('nevt_sumw', axis = 1)
        tbl_nevt = pd.merge(tbl_process, tbl_nevt)
        tbl_nevt = sum_over_categories(tbl_nevt, categories = ('component', ), variables = ('nevt', ))
        tbl_nevt = pd.merge(tbl_nevt, tbl_xsec)

    tbl = pd.merge(tbl, tbl_nevt)
    if use_nevt_sumw:
        tbl['xsecvar'] = tbl.nvar*(tbl.xsec/tbl.nevt_sumw)**2
        tbl['xsec'] = tbl.n*(tbl.xsec/tbl.nevt_sumw)
        del tbl['nevt_sumw']
    else:
        tbl['xsecvar'] = tbl.nvar*(tbl.xsec/tbl.nevt)**2
        tbl['xsec'] = tbl.n*(tbl.xsec/tbl.nevt)
        del tbl['nevt']
    del tbl['n']
    del tbl['nvar']

    ret = sum_over_categories(tbl, categories = ('phasespace', ), variables = ('xsec', 'xsecvar'))

    ret = keep_dtype(ret, tbl_process, columns = ['process'])
    ret = keep_dtype(ret, tbl_yield)

    return ret

##__________________________________________________________________||
def stack_counts_categories(tbl, variables, category, order = None,
                            bottom = None, top = None):
    """return a data frame with stacked contents

    This function stacks contents of the data frame by the category in
    an order. It does what ROOT THStack does with histograms.

    By default, the decreasing order of variables will be used as the
    stack order.

    The order of the stack can be controlled by `order`, 'bottom`, or
    'top`. Categories to be stacked in the bottom or top can be
    specified by 'bottom` or 'top`. If `order` is given, it will fully
    specify the the order and `bottom` and `top` will be ignored.

    Args:

    tbl (pandas.DataFrame): the input data frame

    variables (string list): the names of the variables to stack

    category (string): the name of the category by which to stack,
      e.g., "process"

    order (list): a list of values in the category in the order in
      which to stack. The first element will be in the bottom. The
      last element will be in the top.

    bottom (list): a list of values in the category to stack in the
      bottom. The first element will be in the bottom.

    top (list): a list of values in the category to stack in the
      top. The first element will be in the top.

    """

    if order is None:
        d = tbl.groupby(category)[variables].sum().reset_index()
        order = d.sort_values(list(variables))[category]
        order = list(order)
        if bottom is not None:
            for b in bottom:
                if b in order: order.remove(b)
            order = list(bottom) + order
        if top is not None:
            for t in top:
                if t in order: order.remove(t)
            order =  order + list(reversed(top))

    isFirst = True
    stack = 1
    toStack = [ ]
    for o in order:
        if len(tbl[tbl[category] == o]) == 0: continue
        toStack.append(o)
        d = tbl[tbl[category].isin(toStack)].copy()
        d[category] = o
        d = sum_over_categories(d, categories = None, variables = variables)
        d['stack'] = stack
        stack += 1
        if isFirst:
            ret = d
            isFirst = False
        else:
            ret = ret.append(d, ignore_index = True)
    if isFirst: return None

    ret = keep_dtype(ret, tbl)

    return ret

##__________________________________________________________________||
def keep_dtype(dest, src, columns = None):

    columns = dest.columns if columns is None else columns

    for col in columns:
        if not col in src.columns: continue
        if dest[col].dtype is src[col].dtype: continue
        if src[col].dtype.name == 'category':
            dest[col] = dest[col].astype('category',
                                       categories = src[col].cat.categories,
                                       ordered = src[col].cat.ordered)
            continue
        dest[col] = dest[col].astype(src[col].dtype)

    return dest

##__________________________________________________________________||
