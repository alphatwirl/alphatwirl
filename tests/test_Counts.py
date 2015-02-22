#!/usr/bin/env python
from AlphaTwirl import Counts, countsToDataFrame
import pandas
import unittest

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1), check_names = True)

##____________________________________________________________________________||
class TestCounts(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(pandas.core.frame.DataFrame, assertDataFrameEqual)

    def test_counts(self):
        counts = Counts()

        counts.count(1)
        expected  = {1: {'n': 1.0, 'nvar': 1.0}}
        self.assertEqual(expected, counts.counts)

        counts.count(1)
        expected  = {1: {'n': 2.0, 'nvar': 2.0}}
        self.assertEqual(expected, counts.counts)

        counts.count(1, 2)
        expected  = {1: {'n': 4.0, 'nvar': 6.0}}
        self.assertEqual(expected, counts.counts)

        counts.count(2, 3)
        expected  = {1: {'n': 4.0, 'nvar': 6.0}, 2: {'n': 3.0, 'nvar': 9.0}}
        self.assertEqual(expected, counts.counts)

        counts.count(3, 2, 3)
        expected  = {
            1: {'n': 4.0, 'nvar': 6.0},
            2: {'n': 3.0, 'nvar': 9.0},
            3: {'n': 2.0, 'nvar': 3.0},
            }
        self.assertEqual(expected, counts.counts)

    def test_countsToDataFrame(self):

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

    def test_countsToDataFrame_emptyCounts(self):
        counts  = { }
        expected = pandas.DataFrame({'v1': [ ], 'n': [ ], 'nvar': [ ]})
        columns = ("v1", )
        self.assertEqual(expected, countsToDataFrame(counts, columns))

##____________________________________________________________________________||
