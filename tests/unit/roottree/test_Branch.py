from alphatwirl.roottree import Branch
import unittest
import array

##__________________________________________________________________||
class TestBranch(unittest.TestCase):

    def test_repr(self):
        ar = array.array('d', [ 112.4, 87.6, 30.2])
        ca = array.array('i', [ 2 ])
        obj = Branch('jet_pt', ar, ca)
        repr(obj)

    def test_array(self):

        ar = array.array('d', [ 112.4, 87.6, 30.2])
        ca = array.array('i', [ 2 ])
        obj = Branch('jet_pt', ar, ca)

        self.assertEqual(2, len(obj))
        self.assertEqual(112.4, obj[0])
        self.assertEqual(87.6, obj[1])
        self.assertRaises(IndexError, obj.__getitem__, 2)

    def test_value(self):

        ar = array.array('d', [ 112.4])
        ca = None
        obj = Branch('met_pt', ar, ca)

        self.assertEqual(1, len(obj))
        self.assertEqual(112.4, obj[0])
        self.assertRaises(IndexError, obj.__getitem__, 1)

##__________________________________________________________________||
