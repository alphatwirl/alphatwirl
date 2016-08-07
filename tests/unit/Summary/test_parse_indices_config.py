import AlphaTwirl.Summary as Summary
import unittest

##__________________________________________________________________||
class Test_parse_indices_config(unittest.TestCase):

    def test_1(self):
        actual = Summary.parse_indices_config((None, None, '(*)', '(*)', '\\1', '\\2'))
        expected = ([None, None, None, None, 2, 3], [0, 0, '*', '*', '\\1', '\\2'])
        self.assertEqual(expected, actual)

##__________________________________________________________________||
