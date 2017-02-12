import collections
import unittest
import numpy as np

##__________________________________________________________________||
hasPandas = False
try:
    import pandas
    from AlphaTwirl.Collector import countsToDataFrame, CombineIntoPandasDataFrame
    hasPandas = True
except ImportError:
    pass

##__________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort_index(axis = 1), df2.sort_index(axis = 1), check_names = True)

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results

##__________________________________________________________________||
class MockResult(object):
    def __init__(self, results):
        self._results = results

    def results(self):
        return self._results

##__________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class TestCombineIntoPandasDataFrame(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(pandas.core.frame.DataFrame, assertDataFrameEqual)

    def test_combine_oneReader(self):

        reader = MockReader(
            MockResult(
                {
                    (1, ): np.array((4, 6)),
                    (2, ): np.array((3, 9)),
                    (3, ): np.array((2, 3)),
                }
            )
        )
        datasetReaderPairs = [('data1', reader), ]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
            ('data1', 1, 4, 6),
            ('data1', 2, 3, 9),
            ('data1', 3, 2, 3),
        ]

        expected = pandas.DataFrame(
            {
                'component': ['data1', 'data1', 'data1'],
                'v1': [1, 2, 3],
                'n': [4, 3, 2],
                'nvar': [6, 9, 3],
                }
            )

        combine = CombineIntoPandasDataFrame(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_twoReaders(self):

        reader1 = MockReader(
            MockResult(
                {
                    (1, ): np.array((4, 6)),
                    (2, ): np.array((3, 9)),
                    (3, ): np.array((2, 3)),
                }
            )
        )

        reader2 = MockReader(
            MockResult(
                {
                    (2, ): np.array((3, 6)),
                    (4, ): np.array((2, 2)),
                }
            )
        )

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = pandas.DataFrame(
            {
                'component': ['data1', 'data1', 'data1', 'data2', 'data2'],
                'v1': [1, 2, 3, 2, 4],
                'n': [4, 3, 2, 3, 2],
                'nvar': [6, 9, 3, 6, 2],
                }
            )

        combine = CombineIntoPandasDataFrame(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_with_empty_counts(self):

        reader1 = MockReader(
            MockResult(
                {
                    (1, ): np.array((4, 6)),
                    (2, ): np.array((3, 9)),
                    (3, ): np.array((2, 3)),
                }
            )
        )

        reader2 = MockReader(MockResult({}))

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = pandas.DataFrame(
            {
                'component': ['data1', 'data1', 'data1'],
                'v1': [1, 2, 3],
                'n': [4, 3, 2],
                'nvar': [6, 9, 3],
                }
            )

        combine = CombineIntoPandasDataFrame(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_all_empty_counts(self):

        reader1 = MockReader(MockResult({}))

        reader2 = MockReader(MockResult({}))

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        # this will make the index Index([], dtype='object')
        # expected = pandas.DataFrame(
        #     {
        #         'component': [ ],
        #         'v1': [ ],
        #         'n': [ ],
        #         'nvar': [ ],
        #         }
        #     )

        # this will make the index Int64Index([], dtype='int64')
        expected = pandas.DataFrame(
            [],
            columns = ('component', 'v1', 'n', 'nvar')
        )

        combine = CombineIntoPandasDataFrame(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        combine = CombineIntoPandasDataFrame(keyNames = ('v1', ), valNames = ('n', 'nvar'))
        self.assertEqual(None, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
