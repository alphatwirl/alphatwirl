from AlphaTwirl.EventReader import MPEventLoopRunner
import unittest

##____________________________________________________________________________||
class MockReader(object):
    def __init__(self):
        self._results = None

    def setResults(self, results):
        self._results = results

    def results(self):
        return self._results

##____________________________________________________________________________||
class MockEventLoop(object):
    def __init__(self, readers):
        self.readers = readers

    def __call__(self, progressReporter):
        for reader in self.readers:
            reader._results = 3456
        return self.readers

##____________________________________________________________________________||
class TestMPEventLoopRunner(unittest.TestCase):

    def test_begin_end(self):
        runner = MPEventLoopRunner()
        runner.begin()
        runner.end()

    def test_run(self):
        runner = MPEventLoopRunner()
        runner.begin()

        reader1 = MockReader()
        reader2 = MockReader()
        eventLoop = MockEventLoop([reader1, reader2])
        runner.run(eventLoop)

        self.assertIsNone(reader1._results)
        self.assertIsNone(reader2._results)

        runner.end()

        self.assertEqual(3456, reader1._results)
        self.assertEqual(3456, reader2._results)

##____________________________________________________________________________||
