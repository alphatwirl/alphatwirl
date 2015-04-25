from AlphaTwirl import Combine
import collections
import unittest

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self, results): self._results = results
    def results(self): return self._results

##____________________________________________________________________________||
class TestCombine(unittest.TestCase):

    def test_one_reader(self):

        counts  = {
            (1, ): {'n': 4.0, 'nvar': 6.0},
            (2, ): {'n': 3.0, 'nvar': 9.0},
            (3, ): {'n': 2.0, 'nvar': 3.0},
            }

        reader = MockReader(counts)
        datasetReaderPairs = [('data1', reader), ]

        expected  = {
            ('data1', 1): {'n': 4.0, 'nvar': 6.0},
            ('data1', 2): {'n': 3.0, 'nvar': 9.0},
            ('data1', 3): {'n': 2.0, 'nvar': 3.0},
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers(self):

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

        expected  = {
            ('data1', 1): {'n': 4.0, 'nvar': 6.0},
            ('data1', 2): {'n': 3.0, 'nvar': 9.0},
            ('data1', 3): {'n': 2.0, 'nvar': 3.0},
            ('data2', 2): {'n': 3.0, 'nvar': 6.0},
            ('data2', 4): {'n': 2.0, 'nvar': 2.0},
        }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_two_readers_ordered_values(self):

        counts1  = {
            (1, ): collections.OrderedDict((('n', 4.0), ('nvar', 6.0))),
            (2, ): collections.OrderedDict((('n', 3.0), ('nvar', 9.0))),
            (3, ): collections.OrderedDict((('n', 2.0), ('nvar', 3.0))),
            }

        reader1 = MockReader(counts1)

        counts2  = {
            (2, ): collections.OrderedDict((('n', 3.0), ('nvar', 6.0))),
            (4, ): collections.OrderedDict((('n', 2.0), ('nvar', 2.0))),
        }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected  = {
            ('data1', 1): collections.OrderedDict((('n', 4.0), ('nvar', 6.0))),
            ('data1', 2): collections.OrderedDict((('n', 3.0), ('nvar', 9.0))),
            ('data1', 3): collections.OrderedDict((('n', 2.0), ('nvar', 3.0))),
            ('data2', 2): collections.OrderedDict((('n', 3.0), ('nvar', 6.0))),
            ('data2', 4): collections.OrderedDict((('n', 2.0), ('nvar', 2.0))),
        }

        expected  = {
            ('data1', 1): {'n': 4.0, 'nvar': 6.0},
            ('data1', 2): {'n': 3.0, 'nvar': 9.0},
            ('data1', 3): {'n': 2.0, 'nvar': 3.0},
            ('data2', 2): {'n': 3.0, 'nvar': 6.0},
            ('data2', 4): {'n': 2.0, 'nvar': 2.0},
        }

        combine = Combine()
        actual = combine.combine(datasetReaderPairs)
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual.values()[0], collections.OrderedDict)
        self.assertIsInstance(actual.values()[1], collections.OrderedDict)
        self.assertIsInstance(actual.values()[2], collections.OrderedDict)
        self.assertIsInstance(actual.values()[3], collections.OrderedDict)
        self.assertIsInstance(actual.values()[4], collections.OrderedDict)


    def test_two_readers_not_same_object(self):

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

        expected  = {
            ('data1', 1): {'n': 4.0, 'nvar': 6.0},
            ('data1', 2): {'n': 3.0, 'nvar': 9.0},
            ('data1', 3): {'n': 2.0, 'nvar': 3.0},
            ('data2', 2): {'n': 3.0, 'nvar': 6.0},
            ('data2', 4): {'n': 2.0, 'nvar': 2.0},
        }

        combine = Combine()
        actual = combine.combine(datasetReaderPairs)
        self.assertEqual(expected, actual)
        self.assertIsNot(counts1[(1, )], actual[('data1', 1)])

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

        expected  = {
            ('data1', 1): {'n': 4.0, 'nvar': 6.0},
            ('data1', 2): {'n': 3.0, 'nvar': 9.0},
            ('data1', 3): {'n': 2.0, 'nvar': 3.0},
            }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_all_empty_counts(self):

        counts1  = { }

        reader1 = MockReader(counts1)

        counts2  = { }

        reader2 = MockReader(counts2)

        datasetReaderPairs = [('data1', reader1), ('data2', reader2)]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

    def test_combine_empty_pairs(self):

        datasetReaderPairs = [ ]

        expected = { }

        combine = Combine()
        self.assertEqual(expected, combine.combine(datasetReaderPairs))

##____________________________________________________________________________||
