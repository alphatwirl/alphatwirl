import unittest

from alphatwirl.loop import NullCollector

##__________________________________________________________________||
class TestCollector(unittest.TestCase):

    def test_collect(self):
        obj = NullCollector()
        repr(obj)
        self.assertIsNone(obj.collect([]))

##__________________________________________________________________||
