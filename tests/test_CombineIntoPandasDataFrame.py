#!/usr/bin/env python
from AlphaTwirl import countsToDataFrame, CombineIntoPandasDataFrame
import pandas
import unittest

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1), check_names = True)

##____________________________________________________________________________||
class TestCountsToDataFrame(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(pandas.core.frame.DataFrame, assertDataFrameEqual)

    def test_call(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        expected = pandas.DataFrame(
            {
                'v1': [1, 2, 3],
                'n': [4.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0],
                }
            )

        columns = ("v1", )
        self.assertEqual(expected, countsToDataFrame(counts, columns))

    def test_valNames(self):

        counts  = {
            (1, ): {'x': 4.0, 'var_x': 6.0},
            (2, ): {'x': 3.0, 'var_x': 9.0},
            (3, ): {'x': 2.0, 'var_x': 3.0},
            }

        expected = pandas.DataFrame(
            {
                'v1': [1, 2, 3],
                'x': [4.0, 3.0, 2.0],
                'var_x': [6.0, 9.0, 3.0],
                }
            )

        columns = ("v1", )
        valNames = ('x', 'var_x')
        self.assertEqual(expected, countsToDataFrame(counts, columns, valNames))

    def test_emptyCounts(self):
        counts  = { }
        expected = pandas.DataFrame({'v1': [ ], 'n': [ ], 'nvar': [ ]})
        columns = ("v1", )
        self.assertEqual(expected, countsToDataFrame(counts, columns))

##____________________________________________________________________________||
