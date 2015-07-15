import unittest
import cStringIO

##____________________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    from AlphaTwirl.Aggregate import combine_MC_yields_in_datasets_into_xsec_in_processes
    hasPandas = True
except ImportError:
    class PD:
        def read_table(self, *args, **kargs): pass
    pd = PD()

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1),
                              check_less_precise = True, check_names = True)

##____________________________________________________________________________||
tbl_component_met = pd.read_table(cStringIO.StringIO(
"""component  njets   HT         MET   n  nvar
      QCD_HT_1000ToInf      4  800  125.892541   1     1
      QCD_HT_1000ToInf      5  800  114.815362   1     1
      QCD_HT_1000ToInf      5  800  125.892541   1     1
      QCD_HT_1000ToInf      5  800  131.825674   1     1
      QCD_HT_1000ToInf      5  800  138.038426   1     1
 QCD_HT_1000ToInf_ext1      4  800  114.815362   1     1
 QCD_HT_1000ToInf_ext1      5  800  104.712855   1     1
 QCD_HT_1000ToInf_ext1      5  800  120.226443   2     2
 QCD_HT_1000ToInf_ext1      5  800  125.892541   1     1
 QCD_HT_1000ToInf_ext1      5  800  144.543977   1     1
      QCD_HT_500To1000      5  800  144.543977   1     1
             TBar_tWch      4  800  125.892541   1     1
             TBar_tWch      5  800  114.815362   1     1
             TBar_tWch      5  800  120.226443   1     1
             TBar_tWch      5  800  131.825674   3     3
             TBar_tWch      5  800  138.038426   2     2
             TBar_tWch      5  800  144.543977   2     2
                TTJets      4  800  114.815362   7     7
                TTJets      4  800  120.226443   6     6
                TTJets      4  800  125.892541   6     6
                TTJets      4  800  131.825674   7     7
                TTJets      4  800  138.038426  11    11
                TTJets      4  800  144.543977  12    12
                TTJets      5  600  144.543977   2     2
                TTJets      5  800  104.712855   5     5
                TTJets      5  800  109.647820  15    15
                TTJets      5  800  114.815362  28    28
                TTJets      5  800  120.226443  34    34
                TTJets      5  800  125.892541  37    37
                TTJets      5  800  131.825674  60    60
                TTJets      5  800  138.038426  72    72
                TTJets      5  800  144.543977  74    74
                T_tWch      4  800  131.825674   2     2
                T_tWch      4  800  138.038426   1     1
                T_tWch      5  800  120.226443   1     1
                T_tWch      5  800  125.892541   4     4
                T_tWch      5  800  131.825674   1     1
                T_tWch      5  800  138.038426   3     3
                T_tWch      5  800  144.543977   2     2
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_process = pd.read_table(cStringIO.StringIO(
"""             component             phasespace  process
      QCD_HT_500To1000       QCD_HT_500To1000  QCD
      QCD_HT_1000ToInf       QCD_HT_1000ToInf  QCD
 QCD_HT_500To1000_ext1       QCD_HT_500To1000  QCD
 QCD_HT_1000ToInf_ext1       QCD_HT_1000ToInf  QCD
                T_tWch                 T_tWch  T
             TBar_tWch              TBar_tWch  T
                TTJets                 TTJets  TTJets
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_xsec = pd.read_table(cStringIO.StringIO(
"""             component     xsec
      QCD_HT_1000ToInf    769.7
 QCD_HT_1000ToInf_ext1    769.7
      QCD_HT_500To1000    26740
 QCD_HT_500To1000_ext1    26740
                T_tWch     35.6
             TBar_tWch     35.6
                TTJets    809.1
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_nevt = pd.read_table(cStringIO.StringIO(
"""             component     nevt     nevt_sumw
      QCD_HT_1000ToInf  1130720       1130720
 QCD_HT_1000ToInf_ext1   333733        333733
      QCD_HT_500To1000  3214312       3214312
 QCD_HT_500To1000_ext1   849033        849033
                T_tWch   986100        986100
             TBar_tWch   971800        971800
                TTJets 25446993      25446993
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_process_met = pd.read_table(cStringIO.StringIO(
"""process  njets   HT         MET      xsec       xsecvar
    QCD      4  800  114.815362 5.255887e-04  2.762435e-07
    QCD      4  800  125.892541 5.255887e-04  2.762435e-07
    QCD      5  800  104.712855 5.255887e-04  2.762435e-07
    QCD      5  800  114.815362 5.255887e-04  2.762435e-07
    QCD      5  800  120.226443 1.051177e-03  5.524870e-07
    QCD      5  800  125.892541 1.051177e-03  5.524870e-07
    QCD      5  800  131.825674 5.255887e-04  2.762435e-07
    QCD      5  800  138.038426 5.255887e-04  2.762435e-07
    QCD      5  800  144.543977 7.106374e-03  4.358298e-05
      T      4  800  125.892541 3.663305e-05  1.341981e-09
      T      4  800  131.825674 7.220363e-05  2.606682e-09
      T      4  800  138.038426 3.610182e-05  1.303341e-09
      T      5  800  114.815362 3.663305e-05  1.341981e-09
      T      5  800  120.226443 7.273487e-05  2.645322e-09
      T      5  800  125.892541 1.444073e-04  5.213364e-09
      T      5  800  131.825674 1.460010e-04  5.329283e-09
      T      5  800  138.038426 1.815715e-04  6.593984e-09
      T      5  800  144.543977 1.454697e-04  5.290643e-09
 TTJets      4  800  114.815362 2.225685e-04  7.076679e-09
 TTJets      4  800  120.226443 1.907730e-04  6.065725e-09
 TTJets      4  800  125.892541 1.907730e-04  6.065725e-09
 TTJets      4  800  131.825674 2.225685e-04  7.076679e-09
 TTJets      4  800  138.038426 3.497506e-04  1.112050e-08
 TTJets      4  800  144.543977 3.815461e-04  1.213145e-08
 TTJets      5  600  144.543977 6.359101e-05  2.021908e-09
 TTJets      5  800  104.712855 1.589775e-04  5.054771e-09
 TTJets      5  800  109.647820 4.769326e-04  1.516431e-08
 TTJets      5  800  114.815362 8.902741e-04  2.830672e-08
 TTJets      5  800  120.226443 1.081047e-03  3.437244e-08
 TTJets      5  800  125.892541 1.176434e-03  3.740530e-08
 TTJets      5  800  131.825674 1.907730e-03  6.065725e-08
 TTJets      5  800  138.038426 2.289276e-03  7.278870e-08
 TTJets      5  800  144.543977 2.352867e-03  7.481061e-08
"""), delim_whitespace = True)

##____________________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class Test_combine_MC_yields_in_datasets_into_xsec_in_processes(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

    def test_one(self):
        expect = tbl_process_met
        actual = combine_MC_yields_in_datasets_into_xsec_in_processes(tbl_component_met, tbl_process, tbl_nevt, tbl_xsec)
        ## print actual.to_string(index = False, formatters={'xsec':'{:e}'.format})
        self.assertEqual(expect, actual)


        ## lumi = 4000
        ## actual['n'] = actual.xsec*lumi
        ## actual['nvar'] = actual.xsecvar*lumi**2
        ## del actual['xsec']
        ## del actual['xsecvar']
        ## self.assertEqual(expect, actual)

    # to test
    #  - unique xsec for phasespaces
    #  - conflicting variable names

##____________________________________________________________________________||
