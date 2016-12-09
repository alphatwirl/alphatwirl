import unittest
import numpy as np

from AlphaTwirl.Summary import Scan

##__________________________________________________________________||
class TestScan(unittest.TestCase):

    def test_init(self):
        obj = Scan(val = [10, 20])
        self.assertEqual([[10, 20]], obj.contents)

    def test_init_weight(self): # no effect
        obj = Scan(val = [10, 20], weight = 2)
        self.assertEqual([[10, 20]], obj.contents)

    def test_init_contents(self):
        obj = Scan(contents = [[10, 20], [30, 40]])
        self.assertEqual([[10, 20], [30, 40]], obj.contents)

    def test_init_None(self):
        obj = Scan()
        self.assertEqual([], obj.contents)

    def test_add(self):
        obj1 = Scan(contents = [[10, 20], [30, 40]])
        obj2 = Scan(contents = [[50, 60], [70, 80]])
        obj3 =  obj1 + obj2
        self.assertEqual([[10, 20], [30, 40], [50, 60], [70, 80]], obj3.contents)
        self.assertIsNot(obj1, obj3)
        self.assertIsNot(obj1.contents, obj3.contents)
        self.assertIsNot(obj2, obj3)
        self.assertIsNot(obj2.contents, obj3.contents)

##__________________________________________________________________||
