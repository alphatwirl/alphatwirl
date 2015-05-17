from AlphaTwirl import AlphaTwirl
import unittest

##____________________________________________________________________________||
class MockComponentReader(object):
    pass

##____________________________________________________________________________||
class TestAlphaTwirl(unittest.TestCase):

    def test_init(self):
        alphaTwirl = AlphaTwirl()

    def test_ArgumentParser(self):
        alphaTwirl = AlphaTwirl()
        alphaTwirl.ArgumentParser()

    def test_addComponentReader(self):
        alphaTwirl = AlphaTwirl()
        componentReader = MockComponentReader()
        alphaTwirl.addComponentReader(componentReader)

##____________________________________________________________________________||
