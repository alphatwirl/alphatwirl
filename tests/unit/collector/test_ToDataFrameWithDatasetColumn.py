# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

##__________________________________________________________________||
has_no_pandas = False
try:
    import pandas as pd
except ImportError:
    has_no_pandas = True

pytestmark = pytest.mark.skipif(has_no_pandas, reason="has no pandas")

from .mock import MockReader, MockSummarizer

if not has_no_pandas:
    from pandas.util.testing import assert_frame_equal
    from alphatwirl.collector import ToDataFrameWithDatasetColumn

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return ToDataFrameWithDatasetColumn(
        summaryColumnNames=('htbin', 'njetbin', 'n', 'nvar'),
        datasetColumnName = 'dataset'
    )

def test_repr(obj):
    repr(obj)

def test_example(obj):
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

    actual = obj.combine(dataset_readers_list)
    assert_frame_equal(expected.sort_index(axis = 1), actual.sort_index(axis = 1), check_names=True)

def test_combine_all_empty_counts(obj):
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

    actual = obj.combine(dataset_readers_list)
    assert_frame_equal(expected.sort_index(axis = 1), actual.sort_index(axis = 1), check_names=True)

def test_combine_empty_pairs(obj):

    dataset_readers_list = [
    ]

    actual = obj.combine(dataset_readers_list)
    assert actual is None

##__________________________________________________________________||
