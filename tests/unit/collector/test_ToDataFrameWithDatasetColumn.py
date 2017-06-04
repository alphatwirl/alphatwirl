import unittest

##__________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    hasPandas = True
except ImportError:
    pass

if hasPandas:
    from alphatwirl.collector import ToDataFrameWithDatasetColumn

from .mock import MockReader, MockSummarizer

##__________________________________________________________________||
def assertDataFrameEqual(df1, df2, **kwds):
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort_index(axis = 1), df2.sort_index(axis = 1), check_names = True)

##__________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class TestToDataFrameWithDatasetColumn(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(pd.core.frame.DataFrame, assertDataFrameEqual)

        self.obj = ToDataFrameWithDatasetColumn(
            summaryColumnNames = ('htbin', 'njetbin', 'n', 'nvar'),
            datasetColumnName = 'dataset'
        )

    def test_repr(self):
        repr(self.obj)

    def test_example(self):

        reader1 = MockReader(
            MockSummarizer(
                [
                    (200, 2, 120, 240),
                ]))

        reader2 = MockReader(
            MockSummarizer(
                [
                    (300, 2, 490, 980),
                    (300, 3, 210, 420),
                ]))

        reader3 = MockReader(
            MockSummarizer(
                [
                    (300, 2, 20, 40),
                    (300, 3, 15, 30),
                ]))

        reader4 = MockReader(MockSummarizer([]))

        dataset_readers_list = [
            ('QCD', (reader1, reader2)),
            ('TTJets', (reader3, )),
            ('WJets', (reader4, )),
            ('ZJets', ( )),
        ]

        expected = pd.DataFrame(
            {
                'dataset': ['QCD', 'QCD', 'QCD', 'TTJets', 'TTJets'],
                'htbin': [200, 300, 300, 300, 300],
                'njetbin': [2, 2, 3, 2, 3],
                'n': [120, 490, 210, 20, 15],
                'nvar': [240, 980, 420, 40, 30],
            })

        actual = self.obj.combine(dataset_readers_list)
        self.assertEqual(expected, actual)

    def test_combine_all_empty_counts(self):

        reader1 = MockReader(MockSummarizer([]))
        reader2 = MockReader(MockSummarizer([]))

        dataset_readers_list = [
            ('data1', (reader1, )),
            ('data2', (reader2, )),
        ]

        # # this will make the index Index([], dtype='object')
        # expected = pd.DataFrame(
        #     {
        #         'dataset': [ ],
        #         'htbin': [ ],
        #         'njetbin': [ ],
        #         'n': [ ],
        #         'nvar': [ ],
        #         }
        #     )

        # this will make the index Int64Index([], dtype='int64')
        expected = pd.DataFrame(
             [],
             columns = ('dataset', 'htbin', 'njetbin', 'n', 'nvar')
        )

        actual = self.obj.combine(dataset_readers_list)
        self.assertEqual(expected, actual)

    def test_combine_empty_pairs(self):

        dataset_readers_list = [
        ]

        actual = self.obj.combine(dataset_readers_list)
        self.assertEqual(None, actual)

##__________________________________________________________________||
