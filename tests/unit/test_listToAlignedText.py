from AlphaTwirl import listToAlignedText
import unittest

##____________________________________________________________________________||
class TestListToAlignedText(unittest.TestCase):

    def test_one(self):

        src = [
            ('component', 'v1', 'nvar', 'n'),
            ('data1',  100, 6.0,   40),
            ('data1',    2, 9.0, 3.3),
            ('data1', 3124, 3.0, 0.0000001),
            ('data2',  333, 6.0, 300909234),
            ('data2',   11, 2.0, 323432.2234),
        ]

        actual = listToAlignedText(src)

        expected = """ component   v1 nvar           n
     data1  100    6          40
     data1    2    9         3.3
     data1 3124    3       1e-07
     data2  333    6   300909234
     data2   11    2 323432.2234
"""

        self.assertEqual(expected, actual)

    def test_empty(self):

        src = [
            ('component', 'v1', 'nvar', 'n'),
        ]

        actual = listToAlignedText(src)

        expected = " component v1 nvar n\n"
        self.assertEqual(expected, actual)

##____________________________________________________________________________||
