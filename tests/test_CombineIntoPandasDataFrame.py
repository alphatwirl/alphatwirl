from AlphaTwirl import countsToDataFrame, CombineIntoPandasDataFrame
import pandas
import collections
import unittest

##____________________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort(axis = 1), df2.sort(axis = 1), check_names = True)

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, results):
        self._results = results

    def keynames(self):
        return ('v1', )

    def valNames(self):
        return ('n', 'nvar')

    def results(self):
        return self._results

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
        df = countsToDataFrame(counts, columns)
        self.assertEqual(expected, countsToDataFrame(counts, columns))

    def test_call_ordered_values(self):

        counts  = {
            (1, ): collections.OrderedDict((('n', 4.0), ('nvar', 6.0))),
            (2, ): collections.OrderedDict((('n', 3.0), ('nvar', 9.0))),
            (3, ): collections.OrderedDict((('n', 2.0), ('nvar', 3.0))),
            }

        expected = pandas.DataFrame(
            {
                'v1': [1, 2, 3],
                'n': [4.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0],
                }
            )

        columns = ("v1", )
        df = countsToDataFrame(counts, columns)
        self.assertEqual(expected, df)
        self.assertEqual(['v1', 'n', 'nvar'], df.columns.values.tolist())

    def test_call_threeValues(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0, 'skewness': 2.3 },
            (2, ): {'n': 3.0, 'nvar': 9.0, 'skewness': 5.4 },
            (3, ): {'n': 2.0, 'nvar': 3.0, 'skewness': 3.6 },
            }

        expected = pandas.DataFrame(
            {
                'v1': [1, 2, 3],
                'n': [4.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0],
                'skewness': [2.3, 5.4, 3.6],
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
class TestCombineIntoPandasDataFrame(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(pandas.core.frame.DataFrame, assertDataFrameEqual)

    def test_combine_oneReader(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        reader = MockReader(counts)
        datasetReaderPairs = [('data1', reader), ]

        expected = pandas.DataFrame(
            {
                'component': ['data1', 'data1', 'data1'],
                'v1': [1, 2, 3],
                'n': [4.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0],
                }
            )

        combine = CombineIntoPandasDataFrame()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_twoReaders(self):

        counts1  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        reader1 = MockReader(counts1)

        counts2  = {
            (2, ): {'n': 3.0, 'nvar': 6.0},
            (4, ): {'n': 2.0, 'nvar': 2.0},
            }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = pandas.DataFrame(
            {
                'component': ['data1', 'data1', 'data1', 'data2', 'data2'],
                'v1': [1, 2, 3, 2, 4],
                'n': [4.0, 3.0, 2.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0, 6.0, 2.0],
                }
            )

        combine = CombineIntoPandasDataFrame()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

##____________________________________________________________________________||
