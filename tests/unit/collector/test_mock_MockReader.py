import unittest

from .mock import MockReader, MockSummarizer

##__________________________________________________________________||
class TestMockReader(unittest.TestCase):

    def setUp(self):
        self.summarizer = MockSummarizer([])
        self.obj = MockReader(self.summarizer)

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_results(self):
        self.assertIs(self.summarizer, self.obj.results())

##__________________________________________________________________||
