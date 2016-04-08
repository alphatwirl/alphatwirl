import unittest
import cStringIO

##__________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    from AlphaTwirl.Aggregate import stack_counts_categories
    hasPandas = True
except ImportError:
    class PD:
        def read_table(self, *args, **kargs): pass
    pd = PD()

##__________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort_index(axis = 1), df2.sort_index(axis = 1),
                              check_less_precise = True, check_names = True)

##__________________________________________________________________||
tbl_process = pd.read_table(cStringIO.StringIO(
"""    process  nBJet40          n          nvar  luminosity
 DYJetsToLL        0   0.950682  1.078378e-03           1
 DYJetsToLL        1   0.156116  1.868890e-04           1
 DYJetsToLL        2   0.018499  2.300486e-05           1
 DYJetsToLL        3   0.001805  1.221497e-06           1
 DYJetsToLL        4   0.000000  0.000000e+00           1
        QCD        0   3.049929  2.827426e-01           1
        QCD        1   3.044325  8.633838e-01           1
        QCD        2   0.220113  2.104994e-02           1
        QCD        3   0.000676  2.234952e-07           1
        QCD        4   0.000000  0.000000e+00           1
     TTJets        0   2.573971  4.288517e-04           1
     TTJets        1   6.839210  1.139487e-03           1
     TTJets        2   4.743245  7.902762e-04           1
     TTJets        3   0.572808  9.543608e-05           1
     TTJets        4   0.028824  4.802339e-06           1
     TTJets        5   0.001833  3.053510e-07           1
     TTJets        6   0.000167  2.775919e-08           1
     TTJets        7   0.000000  0.000000e+00           1
 WJetsToLNu        0  23.409848  2.370413e-01           1
 WJetsToLNu        1   4.115114  3.960217e-02           1
 WJetsToLNu        2   0.302472  2.942274e-03           1
 WJetsToLNu        3   0.014937  5.577770e-05           1
 WJetsToLNu        4   0.000000  0.000000e+00           1
"""), delim_whitespace = True)

tbl_process['process'] = tbl_process[:]['process'].astype('category', ordered = True)
tbl_process['nBJet40'] = tbl_process[:]['nBJet40'].astype('category', ordered = True)

##__________________________________________________________________||
tbl_stack_process = pd.read_table(cStringIO.StringIO(
"""       process  nBJet40  luminosity          n          nvar  stack
       QCD        0           1   3.049929  2.827426e-01      1
       QCD        1           1   3.044325  8.633838e-01      1
       QCD        2           1   0.220113  2.104994e-02      1
       QCD        3           1   0.000676  2.234952e-07      1
       QCD        4           1   0.000000  0.000000e+00      1
DYJetsToLL        0           1   4.000611  2.838210e-01      2
DYJetsToLL        1           1   3.200441  8.635707e-01      2
DYJetsToLL        2           1   0.238612  2.107294e-02      2
DYJetsToLL        3           1   0.002481  1.444992e-06      2
DYJetsToLL        4           1   0.000000  0.000000e+00      2
    TTJets        0           1   6.574582  2.842498e-01      3
    TTJets        1           1  10.039651  8.647102e-01      3
    TTJets        2           1   4.981857  2.186322e-02      3
    TTJets        3           1   0.575289  9.688107e-05      3
    TTJets        4           1   0.028824  4.802339e-06      3
    TTJets        5           1   0.001833  3.053510e-07      3
    TTJets        6           1   0.000167  2.775919e-08      3
    TTJets        7           1   0.000000  0.000000e+00      3
WJetsToLNu        0           1  29.984430  5.212911e-01      4
WJetsToLNu        1           1  14.154765  9.043123e-01      4
WJetsToLNu        2           1   5.284329  2.480550e-02      4
WJetsToLNu        3           1   0.590226  1.526588e-04      4
WJetsToLNu        4           1   0.028824  4.802339e-06      4
WJetsToLNu        5           1   0.001833  3.053510e-07      4
WJetsToLNu        6           1   0.000167  2.775919e-08      4
WJetsToLNu        7           1   0.000000  0.000000e+00      4
"""), delim_whitespace = True)

tbl_stack_process['process'] = tbl_stack_process[:]['process'].astype('category', ordered = True)
tbl_stack_process['nBJet40'] = tbl_stack_process[:]['nBJet40'].astype('category', ordered = True)

##__________________________________________________________________||
tbl_stack_process_order = pd.read_table(cStringIO.StringIO(
"""       process  nBJet40  luminosity          n          nvar  stack
DYJetsToLL        0           1   0.950682  1.078378e-03      1
DYJetsToLL        1           1   0.156116  1.868890e-04      1
DYJetsToLL        2           1   0.018499  2.300486e-05      1
DYJetsToLL        3           1   0.001805  1.221497e-06      1
DYJetsToLL        4           1   0.000000  0.000000e+00      1
       QCD        0           1   4.000611  2.838210e-01      2
       QCD        1           1   3.200441  8.635707e-01      2
       QCD        2           1   0.238612  2.107294e-02      2
       QCD        3           1   0.002481  1.444992e-06      2
       QCD        4           1   0.000000  0.000000e+00      2
    TTJets        0           1   6.574582  2.842498e-01      3
    TTJets        1           1  10.039651  8.647102e-01      3
    TTJets        2           1   4.981857  2.186322e-02      3
    TTJets        3           1   0.575289  9.688107e-05      3
    TTJets        4           1   0.028824  4.802339e-06      3
    TTJets        5           1   0.001833  3.053510e-07      3
    TTJets        6           1   0.000167  2.775919e-08      3
    TTJets        7           1   0.000000  0.000000e+00      3
WJetsToLNu        0           1  29.984430  5.212911e-01      4
WJetsToLNu        1           1  14.154765  9.043123e-01      4
WJetsToLNu        2           1   5.284329  2.480550e-02      4
WJetsToLNu        3           1   0.590226  1.526588e-04      4
WJetsToLNu        4           1   0.028824  4.802339e-06      4
WJetsToLNu        5           1   0.001833  3.053510e-07      4
WJetsToLNu        6           1   0.000167  2.775919e-08      4
WJetsToLNu        7           1   0.000000  0.000000e+00      4
"""), delim_whitespace = True)

tbl_stack_process_order['process'] = tbl_stack_process_order[:]['process'].astype('category', ordered = True)
tbl_stack_process_order['nBJet40'] = tbl_stack_process_order[:]['nBJet40'].astype('category', ordered = True)

##__________________________________________________________________||
tbl_stack_process_bottom = pd.read_table(cStringIO.StringIO(
"""       process  nBJet40  luminosity          n          nvar  stack
    TTJets        0           1   2.573971  4.288517e-04      1
    TTJets        1           1   6.839210  1.139487e-03      1
    TTJets        2           1   4.743245  7.902762e-04      1
    TTJets        3           1   0.572808  9.543608e-05      1
    TTJets        4           1   0.028824  4.802339e-06      1
    TTJets        5           1   0.001833  3.053510e-07      1
    TTJets        6           1   0.000167  2.775919e-08      1
    TTJets        7           1   0.000000  0.000000e+00      1
       QCD        0           1   5.623900  2.831715e-01      2
       QCD        1           1   9.883535  8.645233e-01      2
       QCD        2           1   4.963358  2.184022e-02      2
       QCD        3           1   0.573484  9.565958e-05      2
       QCD        4           1   0.028824  4.802339e-06      2
       QCD        5           1   0.001833  3.053510e-07      2
       QCD        6           1   0.000167  2.775919e-08      2
       QCD        7           1   0.000000  0.000000e+00      2
DYJetsToLL        0           1   6.574582  2.842498e-01      3
DYJetsToLL        1           1  10.039651  8.647102e-01      3
DYJetsToLL        2           1   4.981857  2.186322e-02      3
DYJetsToLL        3           1   0.575289  9.688107e-05      3
DYJetsToLL        4           1   0.028824  4.802339e-06      3
DYJetsToLL        5           1   0.001833  3.053510e-07      3
DYJetsToLL        6           1   0.000167  2.775919e-08      3
DYJetsToLL        7           1   0.000000  0.000000e+00      3
WJetsToLNu        0           1  29.984430  5.212911e-01      4
WJetsToLNu        1           1  14.154765  9.043123e-01      4
WJetsToLNu        2           1   5.284329  2.480550e-02      4
WJetsToLNu        3           1   0.590226  1.526588e-04      4
WJetsToLNu        4           1   0.028824  4.802339e-06      4
WJetsToLNu        5           1   0.001833  3.053510e-07      4
WJetsToLNu        6           1   0.000167  2.775919e-08      4
WJetsToLNu        7           1   0.000000  0.000000e+00      4
"""), delim_whitespace = True)

tbl_stack_process_bottom['process'] = tbl_stack_process_bottom[:]['process'].astype('category', ordered = True)
tbl_stack_process_bottom['nBJet40'] = tbl_stack_process_bottom[:]['nBJet40'].astype('category', ordered = True)

##__________________________________________________________________||
tbl_stack_process_top = pd.read_table(cStringIO.StringIO(
"""       process  nBJet40  luminosity          n          nvar  stack
DYJetsToLL        0           1   0.950682  1.078378e-03      1
DYJetsToLL        1           1   0.156116  1.868890e-04      1
DYJetsToLL        2           1   0.018499  2.300486e-05      1
DYJetsToLL        3           1   0.001805  1.221497e-06      1
DYJetsToLL        4           1   0.000000  0.000000e+00      1
WJetsToLNu        0           1  24.360530  2.381197e-01      2
WJetsToLNu        1           1   4.271230  3.978906e-02      2
WJetsToLNu        2           1   0.320971  2.965279e-03      2
WJetsToLNu        3           1   0.016742  5.699920e-05      2
WJetsToLNu        4           1   0.000000  0.000000e+00      2
       QCD        0           1  27.410459  5.208623e-01      3
       QCD        1           1   7.315555  9.031729e-01      3
       QCD        2           1   0.541084  2.401522e-02      3
       QCD        3           1   0.017418  5.722269e-05      3
       QCD        4           1   0.000000  0.000000e+00      3
    TTJets        0           1  29.984430  5.212911e-01      4
    TTJets        1           1  14.154765  9.043123e-01      4
    TTJets        2           1   5.284329  2.480550e-02      4
    TTJets        3           1   0.590226  1.526588e-04      4
    TTJets        4           1   0.028824  4.802339e-06      4
    TTJets        5           1   0.001833  3.053510e-07      4
    TTJets        6           1   0.000167  2.775919e-08      4
    TTJets        7           1   0.000000  0.000000e+00      4
"""), delim_whitespace = True)

tbl_stack_process_top['process'] = tbl_stack_process_top[:]['process'].astype('category', ordered = True)
tbl_stack_process_top['nBJet40'] = tbl_stack_process_top[:]['nBJet40'].astype('category', ordered = True)

##__________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class Test_combine_MC_yields_in_datasets_into_xsec_in_processes(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

    def test_specified_order(self):
        expect = tbl_stack_process
        actual = stack_counts_categories(
            tbl_process,
            variables = ('n', 'nvar'),
            category = 'process',
            order = ('QCD', 'T', 'DYJetsToLL', 'GJets', 'TTJets', 'WJetsToLNu', 'ZJetsToNuNu'),
            )
        self.assertEqual(expect, actual)

    def test_specified_bottom(self):
        expect = tbl_stack_process_bottom
        actual = stack_counts_categories(
            tbl_process,
            variables = ('n', 'nvar'),
            category = 'process',
            bottom = ('TTJets', 'QCD'),
            )
        self.assertEqual(expect, actual)

    def test_specified_top(self):
        expect = tbl_stack_process_top
        actual = stack_counts_categories(
            tbl_process,
            variables = ('n', 'nvar'),
            category = 'process',
            top = ('TTJets', 'QCD'),
            )
        self.assertEqual(expect, actual)

    def test_unspecified_order(self):
        expect = tbl_stack_process_order
        actual = stack_counts_categories(
            tbl_process,
            variables = ('n', 'nvar'),
            category = 'process',
            )
        self.assertEqual(expect, actual)

##__________________________________________________________________||
