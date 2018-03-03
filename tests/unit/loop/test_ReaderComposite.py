# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import ReaderComposite

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return ReaderComposite()

def test_repr(obj):
    repr(obj)

def test_event_two_readers_two_events(obj):
    """
    composite
        |- reader1
        |- reader2
    """
    reader1 = mock.Mock()
    reader2 = mock.Mock()
    obj.add(reader1)
    obj.add(reader2)

    events = mock.Mock()
    obj.begin(events)
    assert [mock.call(events)] == reader1.begin.call_args_list
    assert [mock.call(events)] == reader2.begin.call_args_list

    event1 = mock.Mock()
    obj.event(event1)

    event2 = mock.Mock()
    obj.event(event2)
    assert [mock.call(event1), mock.call(event2)], reader1.events.call_args_list
    assert [mock.call(event1), mock.call(event2)], reader2.events.call_args_list

    obj.end()
    assert [mock.call()] == reader1.end.call_args_list
    assert [mock.call()] == reader2.end.call_args_list

def test_event_nested_composite():
    """
    composite1
        |- composite2
        |      |- reader1
        |      |- reader2
        |- reader3
    """
    obj1 = ReaderComposite()
    obj2 = ReaderComposite()
    reader1 = mock.Mock()
    reader2 = mock.Mock()
    reader3 = mock.Mock()
    obj1.add(obj2)
    obj2.add(reader1)
    obj2.add(reader2)
    obj1.add(reader3)

    events = mock.Mock()
    obj1.begin(events)
    assert [mock.call(events)] == reader1.begin.call_args_list
    assert [mock.call(events)] == reader2.begin.call_args_list
    assert [mock.call(events)] == reader3.begin.call_args_list

    event1 = mock.Mock()
    obj1.event(event1)

    event2 = mock.Mock()
    obj1.event(event2)
    assert [mock.call(event1), mock.call(event2)], reader1.events.call_args_list
    assert [mock.call(event1), mock.call(event2)], reader2.events.call_args_list
    assert [mock.call(event1), mock.call(event2)], reader3.events.call_args_list

    obj1.end()
    assert [mock.call()] == reader1.end.call_args_list
    assert [mock.call()] == reader2.end.call_args_list
    assert [mock.call()] == reader3.end.call_args_list

def test_return_False(obj):
    """
    composite
        |- reader1 (return None)
        |- reader2 (return True)
        |- reader3 (return False)
        |- reader4
    """
    reader1 = mock.Mock()
    reader2 = mock.Mock()
    reader3 = mock.Mock()
    reader4 = mock.Mock()
    obj.add(reader1)
    obj.add(reader2)
    obj.add(reader3)
    obj.add(reader4)

    events = mock.Mock()
    obj.begin(events)

    reader1.event.return_value = None
    reader2.event.return_value = True
    reader3.event.return_value = False

    event1 = mock.Mock()
    ret = obj.event(event1)

    assert [mock.call(event1)], reader1.event.call_args_list
    assert [mock.call(event1)], reader2.event.call_args_list
    assert [mock.call(event1)], reader3.event.call_args_list
    assert [mock.call()], reader4.event.call_args_list
    assert ret is None

    obj.end()

def test_no_begin_end(obj):
    """
    composite
        |- reader1
        |- reader2 (without begin end)
        |- reader3
    """
    reader1 = mock.Mock()

    reader2 = mock.Mock()
    del reader2.begin
    del reader2.end

    reader3 = mock.Mock()
    obj.add(reader1)
    obj.add(reader2)
    obj.add(reader3)

    events = mock.Mock()
    obj.begin(events)
    assert [mock.call(events)] == reader1.begin.call_args_list
    assert [mock.call(events)] == reader3.begin.call_args_list

    event1 = mock.Mock()
    obj.event(event1)

    event2 = mock.Mock()
    obj.event(event2)
    assert [mock.call(event1), mock.call(event2)], reader1.events.call_args_list
    assert [mock.call(event1), mock.call(event2)], reader2.events.call_args_list
    assert [mock.call(event1), mock.call(event2)], reader3.events.call_args_list

    obj.end()
    assert [mock.call()] == reader1.end.call_args_list
    assert [mock.call()] == reader3.end.call_args_list

##__________________________________________________________________||
def test_merge(obj):
    """
    composite
        |- reader1
        |- reader2 (no merge)
        |- reader3
    """
    reader1 = mock.Mock()
    reader2 = mock.Mock()
    reader3 = mock.Mock()
    del reader2.merge

    obj.add(reader1)
    obj.add(reader2)
    obj.add(reader3)

    obj1 = copy.deepcopy(obj)
    assert obj.readers[0] is reader1
    assert obj.readers[1] is reader2
    assert obj.readers[2] is reader3
    assert obj1.readers[0] is not reader1
    assert obj1.readers[1] is not reader2
    assert obj1.readers[2] is not reader3

    obj.merge(obj1)

    assert [mock.call(obj1.readers[0])] == reader1.merge.call_args_list
    assert [mock.call(obj1.readers[2])] == reader3.merge.call_args_list

##__________________________________________________________________||
