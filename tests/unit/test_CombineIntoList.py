from AlphaTwirl import countsToList, CombineIntoList
import collections
import unittest

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, results):
        self._results = results

    def valNames(self):
        return ('n', 'nvar')

    def results(self):
        return self._results

##__________________________________________________________________||
class TestCountsToList(unittest.TestCase):

    def test_call(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
        }

        expected = [
            ('v1', 'nvar', 'n'),
            (1, 6.0, 4.0),
            (2, 9.0, 3.0),
            (3, 3.0, 2.0),
        ]

        columns = ("v1", )
        self.assertEqual(expected, countsToList(counts, columns))

    def test_call_ordered_values(self):

        counts  = {
            (1, ): collections.OrderedDict((('n', 4.0), ('nvar', 6.0))),
            (2, ): collections.OrderedDict((('n', 3.0), ('nvar', 9.0))),
            (3, ): collections.OrderedDict((('n', 2.0), ('nvar', 3.0))),
            }

        expected = [
            ('v1', 'n', 'nvar'),
            (1, 4.0, 6.0),
            (2, 3.0, 9.0),
            (3, 2.0, 3.0),
        ]

        columns = ("v1", )
        self.assertEqual(expected, countsToList(counts, columns))

    def test_call_threeValues(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0, 'skewness': 2.3 },
            (2, ): {'n': 3.0, 'nvar': 9.0, 'skewness': 5.4 },
            (3, ): {'n': 2.0, 'nvar': 3.0, 'skewness': 3.6 },
            }

        expected = [
            ('v1', 'nvar', 'skewness', 'n'),
            (1, 6.0, 2.3, 4.0),
            (2, 9.0, 5.4, 3.0),
            (3, 3.0, 3.6, 2.0)
        ]

        columns = ("v1", )
        self.assertEqual(expected, countsToList(counts, columns))

##__________________________________________________________________||
class TestCombineIntoList(unittest.TestCase):

    def test_combine_oneReader(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        reader = MockReader(counts)
        datasetReaderPairs = [('data1', reader), ]

        expected = [
            ('component', 'v1', 'nvar', 'n'),
            ('data1', 1, 6.0, 4.0),
            ('data1', 2, 9.0, 3.0),
            ('data1', 3, 3.0, 2.0),
        ]

        combine = CombineIntoList(keyNames = ('v1', ))
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

        expected = [
            ('component', 'v1', 'nvar', 'n'),
            ('data1', 1, 6.0, 4.0),
            ('data1', 2, 9.0, 3.0),
            ('data1', 3, 3.0, 2.0),
            ('data2', 2, 6.0, 3.0),
            ('data2', 4, 2.0, 2.0),
        ]

        combine = CombineIntoList(keyNames = ('v1', ))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_with_empty_counts(self):

        counts1  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = [
            ('component', 'v1', 'nvar', 'n'),
            ('data1', 1, 6.0, 4.0),
            ('data1', 2, 9.0, 3.0),
            ('data1', 3, 3.0, 2.0),
        ]

        combine = CombineIntoList(keyNames = ('v1', ))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_all_empty_counts(self):

        counts1  = { }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = [
            ('component', 'v1', 'n', 'nvar'),
        ]

        combine = CombineIntoList(keyNames = ('v1', ))
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        combine = CombineIntoList(keyNames = ('v1', ))
        self.assertEqual(None, combine.combine(datasetReaderPairs))

##__________________________________________________________________||
