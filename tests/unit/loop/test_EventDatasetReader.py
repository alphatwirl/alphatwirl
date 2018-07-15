# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import logging
from collections import OrderedDict

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import EventDatasetReader, EventLoop

##__________________________________________________________________||
@pytest.fixture()
def eventLoopRunner():
    return mock.Mock(name='eventLoopRunner')

@pytest.fixture()
def reader():
    ret = mock.Mock(name='reader')
    ret.configure_mock(name='reader')
    return ret

@pytest.fixture()
def collector():
    return mock.Mock(name='collector')

@pytest.fixture()
def split_into_build_events():
    return mock.Mock(name='split_into_build_events')

@pytest.fixture()
def obj(eventLoopRunner, reader, collector, split_into_build_events):
    return EventDatasetReader(eventLoopRunner, reader, collector,
                                 split_into_build_events)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, eventLoopRunner):
    assert 0 == eventLoopRunner.begin.call_count
    obj.begin()
    assert 1 == eventLoopRunner.begin.call_count

def test_begin_end(obj, eventLoopRunner, collector):
    obj.begin()
    eventLoopRunner.poll.return_value = [ ]
    end = obj.end()
    assert [mock.call([ ])] == collector.collect.call_args_list
    assert collector.collect() == end

def test_standard(obj, eventLoopRunner, reader, collector,
                  split_into_build_events, caplog):

    ## begin
    obj.begin()

    ## create data sets
    # dataset1 - 3 event builders
    build_events1 = mock.Mock(name='build_events1')
    build_events2 = mock.Mock(name='build_events2')
    build_events3 = mock.Mock(name='build_events3')
    dataset1 = mock.Mock(name='dataset1', build_events=[build_events1, build_events2, build_events3])
    dataset1.configure_mock(name='dataset1')

    # dataset2 - no event builder
    dataset2 = mock.Mock(name='dataset2', build_events=[ ])
    dataset2.configure_mock(name='dataset2')

    # dataset3 - 1 event builder
    build_events4 = mock.Mock(name='build_events4')
    dataset3 = mock.Mock(name='dataset3', build_events=[build_events4])
    dataset3.configure_mock(name='dataset3')

    eventLoopRunner.run_multiple.side_effect = [[0, 1, 2], [ ], [3]]
    split_into_build_events.side_effect = lambda dataset: dataset.build_events

    ## read
    obj.read(dataset1)
    obj.read(dataset2)
    obj.read(dataset3)

    assert 0 == eventLoopRunner.run.call_count
    assert 3 == eventLoopRunner.run_multiple.call_count

    call1 = eventLoopRunner.run_multiple.call_args_list[0]

    eventLoop1 = call1[0][0][0]
    assert isinstance(eventLoop1, EventLoop)
    assert build_events1 is eventLoop1.build_events
    assert reader is not eventLoop1.reader
    assert 'reader' == eventLoop1.reader.name

    eventLoop2 = call1[0][0][1]
    assert isinstance(eventLoop2, EventLoop)
    assert build_events2 is eventLoop2.build_events
    assert reader is not eventLoop2.reader
    assert 'reader' == eventLoop2.reader.name

    eventLoop3 = call1[0][0][2]
    assert isinstance(eventLoop3, EventLoop)
    assert build_events3 is eventLoop3.build_events
    assert reader is not eventLoop3.reader
    assert 'reader' == eventLoop3.reader.name

    call2 = eventLoopRunner.run_multiple.call_args_list[1]
    assert mock.call([ ]) == call2

    call3 = eventLoopRunner.run_multiple.call_args_list[2]

    eventLoop4 = call3[0][0][0]
    assert isinstance(eventLoop4, EventLoop)
    assert build_events4 is eventLoop4.build_events
    assert reader is not eventLoop4.reader
    assert 'reader' == eventLoop4.reader.name

    ## end
    eventLoopRunner.receive_one.side_effect = [
        (0, eventLoop1.reader), (1, eventLoop2.reader), (2, eventLoop3.reader), (3, eventLoop4.reader)
    ]
    collector.collect.side_effect = lambda x: x
    assert 0 == eventLoopRunner.receive_one.call_count
    assert 0 == collector.collect.call_count
    results = obj.end()
    assert 4 == eventLoopRunner.receive_one.call_count
    assert 1 == collector.collect.call_count
    expected = [
        ('dataset1', (eventLoop1.reader, eventLoop2.reader, eventLoop3.reader), ),
        ('dataset2', ( )),
        ('dataset3', (eventLoop4.reader, )),
    ]

    # results = [
    #     ('dataset1', [deepcopy(reader)]),
    #     ('dataset2', [deepcopy(reader)]),
    #     ('dataset3', [deepcopy(reader)]),
    # ]

    assert 'dataset1' == results[0][0]
    assert eventLoop1.reader == results[0][1][0]
    assert [
        mock.call(eventLoop2.reader),
        mock.call(eventLoop3.reader)
    ] == eventLoop1.reader.merge.call_args_list

    assert 'dataset2' == results[1][0]

    assert 'dataset3' == results[2][0]
    assert eventLoop4.reader == results[2][1][0]
    assert [
    ] == eventLoop4.reader.merge.call_args_list

@pytest.mark.skip(reason="no longer check the number of the results")
def test_wrong_number_of_results(obj, eventLoopRunner, reader,
                                 collector, split_into_build_events,
                                 caplog):

    reader1 = mock.Mock(name='reader1')
    reader2 = mock.Mock(name='reader2')
    eventLoopRunner.receive_one.side_effect = [reader1, reader2]

    dataset1 = mock.Mock(name='dataset1')
    obj.dataset_nreaders[:] = [(dataset1, 1)]

    with caplog.at_level(logging.WARNING, logger = 'alphatwirl'):
        results = obj.end()

    assert results is None

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'EventDatasetReader' in caplog.records[0].name
    assert 'the same number of' in caplog.records[0].msg

##__________________________________________________________________||
