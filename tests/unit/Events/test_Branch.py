from AlphaTwirl.Events import Branch
import unittest
import array

##__________________________________________________________________||
class TestBranch(unittest.TestCase):

    def test_array(self):

        ar = array.array('d', [ 112.4, 87.6, 30.2])
        ca = array.array('i', [ 2 ])
        jet_pt = Branch('jet_pt', ar, ca)

        self.assertEqual(2, len(jet_pt))
        self.assertEqual(112.4, jet_pt[0])
        self.assertEqual(87.6, jet_pt[1])
        self.assertRaises(IndexError, jet_pt.__getitem__, 2)

    def test_value(self):

        ar = array.array('d', [ 112.4])
        ca = None
        met_pt = Branch('met_pt', ar, ca)

        self.assertEqual(1, len(met_pt))
        self.assertEqual(112.4, met_pt[0])
        self.assertRaises(IndexError, met_pt.__getitem__, 1)

##__________________________________________________________________||
