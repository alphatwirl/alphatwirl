from AlphaTwirl import AlphaTwirl
import unittest

##__________________________________________________________________||
class MockComponentReader(object):
    pass

##__________________________________________________________________||
class TestAlphaTwirl(unittest.TestCase):

    def test_init(self):
        alphaTwirl = AlphaTwirl()

    def test_addComponentReader(self):
        alphaTwirl = AlphaTwirl()
        componentReader = MockComponentReader()
        alphaTwirl.addComponentReader(componentReader)

##__________________________________________________________________||
