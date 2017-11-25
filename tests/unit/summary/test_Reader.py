import unittest
import collections
import logging

import alphatwirl.summary as summary

##__________________________________________________________________||
MockKey = collections.namedtuple('MockKey', 'key')
MockVal = collections.namedtuple('MockVal', 'val')
MockEvent = collections.namedtuple('MockEvent', 'event keys vals')
MockWeight = collections.namedtuple('MockWeight', 'event')

##__________________________________________________________________||
class MockSummarizer(object):
    def __init__(self):
        self.add_called_with = [ ]
        self.add_key_called_with = [ ]
        self.keys_return = [ ]

    def add(self, key, val, weight):
        self.add_called_with.append((key, val, weight))

    def add_key(self, key):
        self.add_key_called_with.append(key)

    def keys(self):
        return self.keys_return

##__________________________________________________________________||
class MockWeightCalculator(object):
    def __call__(self, event):
        return MockWeight(event = event)

##__________________________________________________________________||
class MockKeyValueComposer(object):
    def __init__(self):
        self.began_with = None

    def begin(self, event):
        self.began_with = event

    def __call__(self, event):
        return [(k, v) for k, v in zip(event.keys, event.vals)]

##__________________________________________________________________||
class MockKeyValueComposerRaise(object):
    def __init__(self):
        pass

    def begin(self, event):
        pass

    def __call__(self, event):
        raise Exception('raised by MockKeyValueComposerRaise')

##__________________________________________________________________||
class MockNextKeyComposer(object):
    def __init__(self, nextdic):
        self.nextdic = nextdic

    def __call__(self, key):
        return self.nextdic[key]

##__________________________________________________________________||
class TestReader(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_repr(self):
        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        obj = summary.Reader(keyvalcomposer, summarizer)
        repr(obj)

    def test_begin(self):
        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        obj = summary.Reader(keyvalcomposer, summarizer)
        self.assertIsNone(keyvalcomposer.began_with)
        event = MockEvent(event = 'event1', keys = (), vals = ())
        obj.begin(event)
        self.assertEqual(event, keyvalcomposer.began_with)

    def test_event_raise(self):
        keyvalcomposer = MockKeyValueComposerRaise()
        summarizer = MockSummarizer()
        weightCalculator = MockWeightCalculator()
        obj = summary.Reader(keyvalcomposer, summarizer, weightCalculator = weightCalculator)

        event = MockEvent(event = 'event1', keys = (), vals = ())

        self.assertRaises(Exception, obj.event, event)

    def test_event(self):
        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        weightCalculator = MockWeightCalculator()
        obj = summary.Reader(keyvalcomposer, summarizer, weightCalculator = weightCalculator)

        # two key-val pairs
        key1 = MockKey('key1')
        key2 = MockKey('key2')
        val1 = MockVal('val1')
        val2 = MockVal('val2')

        event = MockEvent(
            event = 'event1',
            keys = (key1, key2),
            vals = (val1, val2)
        )

        obj.event(event)
        self.assertEqual(
            [
                (key1, val1, MockWeight(event)),
                (key2, val2, MockWeight(event)),
            ], summarizer.add_called_with)

        # no key-val pairs
        summarizer.add_called_with[:] = [ ]

        event = MockEvent(event = 'event1', keys = ( ), vals = ( ))

        obj.event(event)
        self.assertEqual([ ], summarizer.add_called_with)

    def test_event_nevents(self):
        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        weightCalculator = MockWeightCalculator()
        obj = summary.Reader(
            keyvalcomposer, summarizer,
            weightCalculator = weightCalculator,
            nevents = 2 # read only first 2 events
        )

        key1 = MockKey('key1')
        val1 = MockVal('val1')

        event1 = MockEvent(event = 'event1', keys = (key1,), vals = (val1, ))
        event2 = MockEvent(event = 'event2', keys = (key1,), vals = (val1, ))
        event3 = MockEvent(event = 'event3', keys = (key1,), vals = (val1, ))

        obj.event(event1)
        obj.event(event2)
        obj.event(event3)
        self.assertEqual(
            [
                (key1, val1, MockWeight(event1)),
                (key1, val1, MockWeight(event2)),
            ], summarizer.add_called_with)


    def test_end(self):
        key1 = MockKey('key1')
        key11 = MockKey('key11')
        key2 = MockKey('key2')
        key21 = MockKey('key21')
        key22 = MockKey('key22')
        key3 = MockKey('key3')
        nextdic = {
            key1: (key11, ),
            key2: (key21, key22),
            key3: ( ),
        }

        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        summarizer.keys_return[:] = [key1, key2, key3]
        nextKeyComposer = MockNextKeyComposer(nextdic)
        obj = summary.Reader(keyvalcomposer, summarizer, nextKeyComposer = nextKeyComposer)
        obj.end()
        self.assertEqual(set([key11, key21, key22]), set(summarizer.add_key_called_with))

    def test_end_None_nextKeyComposer(self):
        key1 = MockKey('key1')
        key2 = MockKey('key2')
        key3 = MockKey('key3')

        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        summarizer.keys_return[:] = [key1, key2, key3]
        nextKeyComposer = None
        obj = summary.Reader(keyvalcomposer, summarizer, nextKeyComposer = nextKeyComposer)
        obj.end()
        self.assertEqual(set([]), set(summarizer.add_key_called_with))

    def test_results(self):
        keyvalcomposer = MockKeyValueComposer()
        summarizer = MockSummarizer()
        obj = summary.Reader(keyvalcomposer, summarizer)
        self.assertIs(summarizer, obj.results())

##__________________________________________________________________||
