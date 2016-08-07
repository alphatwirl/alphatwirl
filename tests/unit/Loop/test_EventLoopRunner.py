from AlphaTwirl.Loop import EventLoopRunner
import unittest

##__________________________________________________________________||
class MockEventLoop(object):
    def __init__(self):
        self.called = False

    def __call__(self, progressReporter):
        self.called = True

##__________________________________________________________________||
class TestEventLoopRunner(unittest.TestCase):

    def setUp(self):
        self.runner = EventLoopRunner()

    def test_begin(self):
        self.runner.begin()

    def test_run(self):
        loop = MockEventLoop()
        self.assertFalse(loop.called)
        self.runner.run(loop)
        self.assertTrue(loop.called)

    def test_end(self):
        self.runner.end()

##__________________________________________________________________||
