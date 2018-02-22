# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import collections
import logging

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.loop import CollectorComposite, ReaderComposite

##__________________________________________________________________||
class MockCollector(object):
    def __init__(self, ret=None):
        self.collected = None
        self.ret = ret

    def collect(self, dataset_readers_list):
        self.collected = dataset_readers_list
        return self.ret

##__________________________________________________________________||
class MockReader(object):
    pass

##__________________________________________________________________||
class MockDataset(object):
    pass

##__________________________________________________________________||
def test_repr():
    obj = CollectorComposite()
    repr(obj)

def test_deprecated_option(caplog):
    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        CollectorComposite(progressReporter=None)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'CollectorComposite' in caplog.records[0].name
    assert 'deprecated' in caplog.records[0].msg

def test_collect():
    """
    1:composite
        |- 2:composite
        |        |- 3:leaf
        |        |- 4:leaf
        |
        |- 5:leaf
    """

    ## build collector
    collector1 = CollectorComposite()
    collector2 = CollectorComposite()
    collector3 = MockCollector('result3')
    collector4 = MockCollector('result4')
    collector5 = MockCollector('result5')

    collector1.add(collector2)
    collector2.add(collector3)
    collector2.add(collector4)
    collector1.add(collector5)

    ## build reader
    reader1 = ReaderComposite()
    reader2 = ReaderComposite()
    reader3 = MockReader()
    reader4 = MockReader()
    reader5 = MockReader()

    reader1.add(reader2)
    reader2.add(reader3)
    reader2.add(reader4)
    reader1.add(reader5)

    ## copy readers
    reader1_copy1 = copy.deepcopy(reader1)
    reader1_copy2 = copy.deepcopy(reader1)
    reader1_copy3 = copy.deepcopy(reader1)
    reader1_copy4 = copy.deepcopy(reader1)

    ## build data set
    dataset1 = MockDataset()
    dataset2 = MockDataset()
    dataset3 = MockDataset()

    assert collector3.collected is None
    assert collector4.collected is None
    assert collector5.collected is None

    dataset_readers_list = [
        (dataset1, (reader1_copy1, reader1_copy2, reader1_copy3)),
        (dataset2, ( )),
        (dataset3, (reader1_copy4, )),
    ]

    assert [
        ['result3', 'result4'],
        'result5'
    ] == collector1.collect(dataset_readers_list)

    assert [
        (dataset1, (reader1_copy1.readers[0].readers[0], reader1_copy2.readers[0].readers[0], reader1_copy3.readers[0].readers[0])),
        (dataset2, ( )),
        (dataset3, (reader1_copy4.readers[0].readers[0], )),
    ] == collector3.collected

    assert [
        (dataset1, (reader1_copy1.readers[0].readers[1], reader1_copy2.readers[0].readers[1], reader1_copy3.readers[0].readers[1])),
        (dataset2, ( )),
        (dataset3, (reader1_copy4.readers[0].readers[1], )),
    ] == collector4.collected

    assert [
        (dataset1, (reader1_copy1.readers[1], reader1_copy2.readers[1], reader1_copy3.readers[1])),
        (dataset2, ( )),
        (dataset3, (reader1_copy4.readers[1], )),
    ] == collector5.collected

##__________________________________________________________________||
