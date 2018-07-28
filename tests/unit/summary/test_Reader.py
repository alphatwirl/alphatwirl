# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import alphatwirl
from alphatwirl.summary import Reader

##__________________________________________________________________||
@pytest.fixture()
def mockKeyValComposer():
    ## ret = mock.Mock(spec=alphatwirl.summary.KeyValueComposer)
    ## ideally, prefer to use spec. However, mock.Mock with spec
    ## sometimes cannot be copied or deep copied in python 2 with mock
    ## 2.0.0. see tests/unit/examples/test_mock.py
    ret = mock.Mock()
    return ret

@pytest.fixture()
def mockSummarizer():
    return mock.MagicMock()

@pytest.fixture()
def mockCollector():
    return mock.Mock()

@pytest.fixture()
def mockNextKeyComposer():
    return mock.Mock()

@pytest.fixture()
def mockWeightCalculator():
    return mock.Mock()

@pytest.fixture()
def obj(mockKeyValComposer, mockSummarizer, mockCollector, mockNextKeyComposer, mockWeightCalculator):
    return Reader(
        mockKeyValComposer, mockSummarizer,
        nextKeyComposer=mockNextKeyComposer,
        collector=mockCollector,
        weightCalculator=mockWeightCalculator
    )

def test_init_without_collector(mockKeyValComposer, mockSummarizer, mockNextKeyComposer, mockWeightCalculator):
    ## possible to init without collector for backward compatibility
    ##
    obj = Reader(
        mockKeyValComposer, mockSummarizer,
        nextKeyComposer=mockNextKeyComposer,
        weightCalculator=mockWeightCalculator
    )

def test_repr(obj):
    repr(obj)

def test_begin(obj, mockKeyValComposer):
    event = mock.Mock()
    obj.begin(event)
    assert [mock.call(event)] == mockKeyValComposer.begin.call_args_list

def test_event_raise(obj, mockKeyValComposer):
    event = mock.Mock()
    mockKeyValComposer.side_effect = Exception
    with pytest.raises(Exception):
        obj.event(event)

def test_event(obj, mockKeyValComposer, mockSummarizer, mockWeightCalculator):
    event = mock.Mock()
    key1 = mock.Mock(name='key1')
    val1 = mock.Mock(name='val1')
    key2 = mock.Mock(name='key2')
    val2 = mock.Mock(name='val2')
    mockKeyValComposer.return_value = [(key1, val1), (key2, val2)]
    weight1 = mock.Mock(name='weight1')
    mockWeightCalculator.return_value = weight1
    obj.event(event)

    assert [
        mock.call(key=key1, val=val1, weight=weight1),
        mock.call(key=key2, val=val2, weight=weight1),
    ] == mockSummarizer.add.call_args_list

    assert [mock.call(event)] == mockKeyValComposer.call_args_list
    assert [mock.call(event)] == mockWeightCalculator.call_args_list

def test_event_nevents(mockKeyValComposer, mockSummarizer, mockWeightCalculator):
    obj = Reader(
        mockKeyValComposer, mockSummarizer,
        weightCalculator=mockWeightCalculator,
        nevents=2 # read only first 2 events
    )

    key1 = mock.Mock(name='key1')
    val1 = mock.Mock(name='val1')
    key2 = mock.Mock(name='key2')
    val2 = mock.Mock(name='val2')
    key3 = mock.Mock(name='key3')
    val3 = mock.Mock(name='val3')
    mockKeyValComposer.side_effect = [[(key1, val1)], [(key2, val2)], [(key3, val3)]]
    weight1 = mock.Mock(name='weight1')
    mockWeightCalculator.return_value = weight1

    event1 = mock.Mock(name='event1')
    event2 = mock.Mock(name='event2')
    event3 = mock.Mock(name='event3')
    obj.event(event1)
    obj.event(event2)
    obj.event(event3)

    assert [
        mock.call(key=key1, val=val1, weight=weight1),
        mock.call(key=key2, val=val2, weight=weight1),
    ] == mockSummarizer.add.call_args_list

    assert [mock.call(event1), mock.call(event2)] == mockKeyValComposer.call_args_list
    assert [mock.call(event1), mock.call(event2)] == mockWeightCalculator.call_args_list

def test_end(obj, mockSummarizer, mockNextKeyComposer):
    key1 = mock.MagicMock(name='key1')
    key2 = mock.MagicMock(name='key2')
    key3 = mock.MagicMock(name='key3')

    key1.__lt__.return_value = True
    key2.__lt__.return_value = True
    key3.__lt__.return_value = True

    key11 = mock.Mock(name='key12')
    key21 = mock.Mock(name='key21')
    key22 = mock.Mock(name='key22')

    mockSummarizer.keys.return_value = [key1, key2, key3]
    mockNextKeyComposer.side_effect = [(key11, ), (key21, key22), ()]
    obj.end()
    assert [
        mock.call(key11), mock.call(key21), mock.call(key22)
    ] == mockSummarizer.add_key.call_args_list

def test_end_None_nextKeyComposer(mockKeyValComposer, mockSummarizer):
    obj = Reader(
        mockKeyValComposer, mockSummarizer,
        nextKeyComposer=None
    )
    key1 = mock.Mock(name='key1')
    key2 = mock.Mock(name='key2')
    key3 = mock.Mock(name='key3')
    mockSummarizer.keys.return_value = [key1, key2, key3]
    obj.end()
    assert [ ] == mockSummarizer.add_key.call_args_list

def test_results(obj, mockSummarizer):
    assert mockSummarizer is obj.results()

def test_merge(obj, mockSummarizer):
    obj1 = copy.deepcopy(obj)

    assert obj1.summarizer is not obj.summarizer
    # note: if just print summarizers like
    # print obj1.summarizer, obj.summarizer
    # the same ids are shown, e.g.,
    # <MagicMock id='4782590736'> <MagicMock id='4782590736'>
    # this is very confusing. they are indeed different objects.
    # the attribute `id` is copied.
    # to print the real id of the copied object, need to print repr()
    # of it.
    # print repr(obj1.summarizer)
    # <MagicMock id='4782590352'>

    obj.merge(obj1)

    assert [mock.call(obj1.summarizer)] == mockSummarizer.__iadd__.call_args_list
    assert obj.summarizer is mockSummarizer.__iadd__()

def test_collect(obj, mockCollector):
    result = obj.collect()
    assert [mock.call(obj)] == mockCollector.call_args_list
    assert mockCollector() is result

##__________________________________________________________________||
