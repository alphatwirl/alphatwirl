import unittest
from alphatwirl.loop import EventLoopRunner

##__________________________________________________________________||
class MockResult(object): pass

##__________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, result):
        self.result = result

    def __call__(self, progressReporter):
        return self.result

##__________________________________________________________________||
class TestEventLoopRunner(unittest.TestCase):

    def setUp(self):
        self.obj = EventLoopRunner()

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):
        self.obj.begin()

    def test_end(self):
        self.obj.begin()
        self.assertEqual([ ], self.obj.end())

    def test_end_without_begin(self):
        self.assertEqual([ ], self.obj.end())

    def test_run(self):
        self.obj.begin()

        result1 = MockResult()
        loop1 = MockEventLoop(result1)
        self.obj.run(loop1)

        result2 = MockResult()
        loop2 = MockEventLoop(result2)
        self.obj.run(loop2)

        self.assertEqual([result1, result2], self.obj.end())

##__________________________________________________________________||
