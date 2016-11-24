import sys
import unittest

from AlphaTwirl.HeppyResult.splitfuncs import *

##__________________________________________________________________||
class TestSplitfuncs(unittest.TestCase):

    def test_start_length_pairs_for_split_lists(self):
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10)], start_length_pairs_for_split_lists(40, 10))
        self.assertEqual([(0, 10), (10, 10), (20, 10), (30, 10), (40, 1)], start_length_pairs_for_split_lists(41, 10))
        self.assertEqual([(0, 40)], start_length_pairs_for_split_lists(40, 40))
        self.assertEqual([(0, 40)], start_length_pairs_for_split_lists(40, 50))

    def test_minimum_positive_value(self):

        # empty
        self.assertEqual(-1, minimum_positive_value([]))

        # all negative
        self.assertEqual(-1, minimum_positive_value([-1, -2, - 3]))

        # all positive
        self.assertEqual(10, minimum_positive_value([10, 20, 30]))

        # zero or positive
        self.assertEqual(0, minimum_positive_value([10, 20, 0, 30]))

        # general
        self.assertEqual(10, minimum_positive_value([10, 20, 30, -2, -3]))

##__________________________________________________________________||
