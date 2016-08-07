import AlphaTwirl.Counter as Counter
import unittest

##__________________________________________________________________||
class MockEvent(object):
    pass

##__________________________________________________________________||
class MockSummary(object):
    def __init__(self):
        self._counts = [ ]
        self._keys = set()
        self._addedkeys = set()

    def add(self, key, val, weight):
        self._counts.append((key, weight))
        self._keys.add(key)

    def keys(self):
        return list(self._keys)

    def addKey(self, key):
        self._addedkeys.add(key)

    def copyFrom(self, src):
        self._counts[:] = src._counts[:]

    def results(self):
        return self._counts

##__________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return 1.0

##__________________________________________________________________||
class MockKeyValueComposer(object):
    def __init__(self, keyval_list = [ ]):
        self.keyval_list = keyval_list
        self._begin = None

    def begin(self, event):
        self._begin = event

    def __call__(self, event):
        return self.keyval_list.pop()

##__________________________________________________________________||
class MockNextKeyComposer(object):
    def __init__(self, nextdic):
        self.nextdic = nextdic

    def __call__(self, key):
        return self.nextdic[key]

##__________________________________________________________________||
class TestMockKeyValueComposer(unittest.TestCase):

    def test_call(self):
        keys = [
            ((10,  5), (101, 22)),
            ((11,  4), (102, 33)),
            ((12,  3), (103, 44)),
            ((13,  2), (104, 55)),
        ]
        keycomposer = MockKeyValueComposer(keys)
        self.assertEqual(((13,  2), (104, 55)), keycomposer(MockEvent()))
        self.assertEqual(((12,  3), (103, 44)), keycomposer(MockEvent()))
        self.assertEqual(((11,  4), (102, 33)), keycomposer(MockEvent()))
        self.assertEqual(((10,  5), (101, 22)), keycomposer(MockEvent()))
        self.assertRaises(IndexError, keycomposer, MockEvent())

##__________________________________________________________________||
class TestCounter(unittest.TestCase):

    def test_events(self):
        summary = MockSummary()
        keyval_list = [
            [((11, ), ()), ((12, ), ())],
            [((12, ), ())],
            [ ],
            [((14, ), ())],
            [((11, ), ())]
        ]
        keycomposer = MockKeyValueComposer(keyval_list)
        nextdic = {(11, ): ((12, ), ), (12, ): ((13, ), ), (14, ): ((15, ), )}
        nextKeyComposer = MockNextKeyComposer(nextdic)
        counter = Counter.Counter(keycomposer, summary, nextKeyComposer, MockWeightCalculator())

        event = MockEvent()
        counter.begin(event)
        self.assertEqual(event, keycomposer._begin)

        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], summary._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], summary._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], summary.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], summary._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0)], summary.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], summary._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0)], summary.results())

        counter.event(MockEvent())
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], summary._counts)
        self.assertEqual([((11,), 1.0), ((14,), 1.0), ((12,), 1.0), ((11,), 1.0), ((12,), 1.0)], summary.results())

        counter.end()
        self.assertEqual(set([(15, ), (13, ), (12, )]), summary._addedkeys)

    def test_default_weight(self):
        summary = MockSummary()
        keyval_list = [
            [((11, ), ()), ((12, ), ())],
            [((12, ), ())],
            [ ],
            [((14, ), ())],
            [((11, ), ())]
        ]
        keycomposer = MockKeyValueComposer(keyval_list)
        nextdic = {(11, ): ((12, ), ), (12, ): ((13, ), ), (14, ): ((15, ), )}
        nextKeyComposer = MockNextKeyComposer(nextdic)
        counter = Counter.Counter(keycomposer, summary, nextKeyComposer)

        self.assertIsInstance(counter.weightCalculator, Counter.WeightCalculatorOne)

        event = MockEvent()
        counter.event(event)
        self.assertEqual([((11, ), 1.0)], summary._counts)
        self.assertEqual([((11, ), 1.0)], counter.results())

    def test_copyFrom(self):
        summary = MockSummary()
        counter = Counter.Counter(MockKeyValueComposer(), summary, MockWeightCalculator())

        src_summary = MockSummary()
        src_counter = Counter.Counter(MockKeyValueComposer(), src_summary, MockWeightCalculator())
        src_summary._counts[:] = [((11, ), 1.0)]

        self.assertEqual([ ], summary._counts)
        counter.copyFrom(src_counter)
        self.assertEqual([((11,), 1.0)], summary._counts)

##__________________________________________________________________||
