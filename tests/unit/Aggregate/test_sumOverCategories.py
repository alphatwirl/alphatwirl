from AlphaTwirl.Aggregate import sumOverCategories
import unittest
import cStringIO

##____________________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    hasPandas = True
except ImportError:
    pass

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1), check_names = True)

##____________________________________________________________________________||
tbl_1_A_B_C = pd.read_table(cStringIO.StringIO(
"""A B C n nvar
a X 2 1   10
a Y 2 2   20
a Z 1 3   30
b X 1 3   30
b X 2 1   10
b Y 1 2   20
b Y 2 3   30
b Z 1 6   60
c X 1 4   40
c X 2 3   30
c Y 1 2   20
c Y 2 2   20
c Y 3 4   40
c Z 1 6   60
c Z 3 3   30
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_1_A_B = pd.read_table(cStringIO.StringIO(
"""A B n nvar
a X 1   10
a Y 2   20
a Z 3   30
b X 4   40
b Y 5   50
b Z 6   60
c X 7   70
c Y 8   80
c Z 9   90
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_1_A = pd.read_table(cStringIO.StringIO(
"""A  n nvar
a  6   60
b 15  150
c 24  240
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_1_B = pd.read_table(cStringIO.StringIO(
"""B  n nvar
X 12  120
Y 15  150
Z 18  180
"""), delim_whitespace = True)

##____________________________________________________________________________||
tbl_1 = pd.read_table(cStringIO.StringIO(
"""n nvar
45  450
"""), delim_whitespace = True)

##____________________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class Test_sumOverCategories(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

    def test_one_category(self):
        expect = tbl_1_A_B
        actual = sumOverCategories(tbl_1_A_B_C, categories = ('C', ), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

    def test_multiple_categories(self):
        expect = tbl_1_A
        actual = sumOverCategories(tbl_1_A_B_C, categories = ('B', 'C'), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

    def test_all_categories(self):
        expect = tbl_1
        actual = sumOverCategories(tbl_1_A_B_C, categories = ('A', 'B', 'C'), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

    def test_all_categories_with_variable_name_index(self):
        expect = tbl_1.rename(columns = {'nvar': 'index'})
        tbl = tbl_1_A_B_C.rename(columns = {'nvar': 'index'})
        actual = sumOverCategories(tbl, categories = ('A', 'B', 'C'), variables = ('n', 'index'))
        self.assertEqual(expect, actual)

    def test_no_categories(self):
        expect = tbl_1_A_B_C
        actual = sumOverCategories(tbl_1_A_B_C, categories = ( ), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

        expect = tbl_1_A_B_C
        actual = sumOverCategories(tbl_1_A_B_C, categories = None, variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

    def test_all_the_way(self):
        expect = tbl_1_A_B
        actual = sumOverCategories(tbl_1_A_B_C, categories = ('C', ), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

        expect = tbl_1_A
        actual = sumOverCategories(tbl_1_A_B, categories = ('B', ), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

        expect = tbl_1
        actual = sumOverCategories(tbl_1_A, categories = ('A', ), variables = ('n', 'nvar'))
        self.assertEqual(expect, actual)

##____________________________________________________________________________||
