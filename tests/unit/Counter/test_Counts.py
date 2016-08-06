from AlphaTwirl.Counter import Counts
import unittest

##__________________________________________________________________||
class TestCounts(unittest.TestCase):

    def test_counts(self):
        counts = Counts()

        counts.count(1)
        expected  = {1: {'n': 1.0, 'nvar': 1.0}}
        self.assertEqual(expected, counts.results())

        counts.count(1)
        expected  = {1: {'n': 2.0, 'nvar': 2.0}}
        self.assertEqual(expected, counts.results())

        counts.count(1, 2)
        expected  = {1: {'n': 4.0, 'nvar': 6.0}}
        self.assertEqual(expected, counts.results())

        counts.count(2, 3)
        expected  = {1: {'n': 4.0, 'nvar': 6.0}, 2: {'n': 3.0, 'nvar': 9.0}}
        self.assertEqual(expected, counts.results())

    def test_copyFrom(self):
        counts = Counts()
        src_counts = Counts()

        expected  = {
            10: {'n': 24.0, 'nvar': 3.0},
            20: {'n': 33.0, 'nvar': 5.0},
            30: {'n': 21.0, 'nvar': 4.0},
            }

        src_counts._counts.update(expected)
        counts.copyFrom(src_counts)
        self.assertEqual(expected, src_counts._counts)
        self.assertIsNot(counts._counts, src_counts._counts)

    def test_valNames(self):
        counts = Counts()
        self.assertEqual(('n', 'nvar'), counts.valNames())

    def test_addKey(self):
        counts = Counts()
        counts.addKey(1)
        expected  = {1: {'n': 0.0, 'nvar': 0.0}}
        self.assertEqual(expected, counts.results())

        counts.addKey(3)
        counts.addKey(5)
        expected  = {1: {'n': 0.0, 'nvar': 0.0},
                     3: {'n': 0.0, 'nvar': 0.0},
                     5: {'n': 0.0, 'nvar': 0.0}}
        self.assertEqual(expected, counts.results())

##__________________________________________________________________||
