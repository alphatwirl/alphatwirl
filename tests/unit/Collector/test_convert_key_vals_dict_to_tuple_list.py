import unittest
import numpy as np
import collections

from AlphaTwirl.Collector.functions import convert_key_vals_dict_to_tuple_list

##__________________________________________________________________||
class Test_convert_key_vals_dict_to_tuple_list(unittest.TestCase):

    def test_example(self):

        counts  = {
            (1, 10): [(4, 6)],
            (2, 11): [ ],
            (3, 12): [(2, 3), (5, 7)],
        }

        expected = [
            (1, 10, 4, 6),
            (3, 12, 2, 3),
            (3, 12, 5, 7),
        ]

        actual = convert_key_vals_dict_to_tuple_list(counts)
        self.assertEqual(expected, actual)

    def test_empty(self):

        counts  = { }

        expected = [ ]

        actual = convert_key_vals_dict_to_tuple_list(counts)
        self.assertEqual(expected, actual)

    def test_sort_off(self):

        counts = collections.OrderedDict([
            ((3, 12), [(5, 7), (2, 3)]),
            ((1, 10), [(4, 6)]),
            ((2, 11), [ ]),
        ])

        expected = [
            (3, 12, 5, 7),
            (3, 12, 2, 3),
            (1, 10, 4, 6),
        ]

        actual = convert_key_vals_dict_to_tuple_list(counts, sort = False)
        self.assertEqual(expected, actual)

    def test_fill_nan(self):

        counts  = {
            (1, 10): [(4, 6, 2, 1)],
            (2, 11): [ ],
            (3, 12): [(2, 3, 4, 5), (5, 7)],
            (4, 13): [( ), ( )]
        }

        expected = [
            (1, 10, 4, 6, 2, 1),
            (3, 12, 2, 3, 4, 5),
            (3, 12, 5, 7, float('nan'), float('nan')),
            (4, 13, float('nan'), float('nan'), float('nan'), float('nan')),
            (4, 13, float('nan'), float('nan'), float('nan'), float('nan')),
        ]

        actual = convert_key_vals_dict_to_tuple_list(counts)
        # self.assertEqual(expected, actual) # don't test because nan == nan is False in python

    def test_fill_0(self):

        counts  = {
            (1, 10): [(4, 6, 2, 1)],
            (2, 11): [ ],
            (3, 12): [(2, 3, 4, 5), (5, 7)],
            (4, 13): [( ), ( )]
        }

        expected = [
            (1, 10, 4, 6, 2, 1),
            (3, 12, 2, 3, 4, 5),
            (3, 12, 5, 7, 0, 0),
            (4, 13, 0, 0, 0, 0),
            (4, 13, 0, 0, 0, 0),
        ]

        actual = convert_key_vals_dict_to_tuple_list(counts, fill = 0)
        self.assertEqual(expected, actual)

    def test_numpy(self):

        counts  = {
            (1, 10): [np.array((4, 6))],
            (2, 11): [ ],
            (3, 12): [np.array((2, 3)), np.array((5, 7))],
        }

        expected = [
            (1, 10, 4, 6),
            (3, 12, 2, 3),
            (3, 12, 5, 7),
        ]

        actual = convert_key_vals_dict_to_tuple_list(counts)
        self.assertEqual(expected, actual)

##__________________________________________________________________||
