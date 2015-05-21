import AlphaTwirl.Counter as Counter
import unittest

##____________________________________________________________________________||
class MockCounts(Counter.CountsBase):
    def __init__(self):
        self._counts = [ ]
        self._keys = [ ]

    def count(self, key, weight): self._counts.append((key, weight))
    def valNames(self): return ('n', 'nvar')
    def addKeys(self, keys): self._keys.append(keys)
    def setResults(self, results): self._counts = results
    def results(self): return self._counts

##____________________________________________________________________________||
class MockNextKeyComposer(object):
    def __init__(self):
        self.keys = [ ]
        self.nexts = [ ]

    def __call__(self, key):
        self.keys.append(key)
        return self.nexts.pop()

##____________________________________________________________________________||
class MockKey(object):
    def __init__(self, i): self._i = i
    def __repr__(self): return "key" + str(self._i)

##____________________________________________________________________________||
class TestCountsWithEmptyNextKeys(unittest.TestCase):

    def test_count_one_bin(self):
        counts = MockCounts()
        countsWENK = Counter.CountsWithEmptyNextKeys(counts)

        keyComposer = MockNextKeyComposer()
        countsWENK.nextKeyComposer = keyComposer

        key1 = MockKey(1)
        key2 = MockKey(2)
        key3 = MockKey(3)

        keyComposer.nexts = [[key2, key3]]
        countsWENK.count(key1, 1)
        self.assertEqual([key1], keyComposer.keys)
        self.assertEqual([(key1, 1.0)], counts._counts)
        self.assertEqual([[key2, key3]], counts._keys)

    def test_results(self):
        counts = MockCounts()
        countsWENK = Counter.CountsWithEmptyNextKeys(counts)
        self.assertEqual([ ], countsWENK.results())

        key1 = MockKey(1)
        countsWENK.setResults([(key1, 3.0)])
        self.assertEqual([(key1, 3.0)], countsWENK.results())

##____________________________________________________________________________||
class TestCountsWithEmptyNextKeysBuilder(unittest.TestCase):

    def test_call(self):
        builder = Counter.CountsWithEmptyNextKeysBuilder(MockCounts)
        counts1 = builder()
        counts2 = builder()
        self.assertIsInstance(counts1, Counter.CountsWithEmptyNextKeys)
        self.assertIsInstance(counts1._countMethod, MockCounts)
        self.assertIsNot(counts1, counts2)
        self.assertIsNot(counts1._countMethod, counts2._countMethod)

##____________________________________________________________________________||
