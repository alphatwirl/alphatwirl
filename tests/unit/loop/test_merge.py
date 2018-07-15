# Tai Sakuma <tai.sakuma@gmail.com>
from collections import OrderedDict

import pytest

from alphatwirl.loop.merge import merge_in_order

##__________________________________________________________________||
class MockData(object):
    def __init__(self, name):
        self.name = name
        self.merged = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('name', self.name),
            ('merged', self.merged),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def merge(self, data_):
        self.merged.extend([data_.name] + data_.merged)


@pytest.mark.parametrize('orders', [
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
    [1, 2, 4, 3, 0, 5],
])
def test_merge_in_order_six_data(orders):
    ndata = 6
    map_ = OrderedDict([(i, None) for i in range(ndata)])

    data = [MockData(name='data{}'.format(i)) for i in range(ndata)]

    for i in orders:
        merge_in_order(map_, i, data[i])

    assert ['data1', 'data2', 'data3', 'data4', 'data5'] == data[0].merged

@pytest.mark.parametrize('orders', [
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
    [1, 2, 4, 3, 0, 5],
])
def test_merge_in_order_six_data_id_shifted(orders):
    ndata = 6
    map_ = OrderedDict([(i + 1000, None) for i in range(ndata)])

    data = [MockData(name='data{}'.format(i)) for i in range(ndata)]

    for i in orders:
        id_ = i + 1000
        merge_in_order(map_, id_, data[i])

    assert ['data1', 'data2', 'data3', 'data4', 'data5'] == data[0].merged

def test_merge_in_order_one_data():
    ndata = 1
    map_ = OrderedDict([(1000, None)])
    data = [MockData(name='data0')]
    merge_in_order(map_, 1000, data[0])

    assert [ ] == data[0].merged

##__________________________________________________________________||
class MockDataWoMerge(object):
    def __init__(self, name):
        self.name = name
        self.merged = [ ]

    def __repr__(self):
        name_value_pairs = (
            ('name', self.name),
            ('merged', self.merged),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

@pytest.mark.parametrize('orders', [
    [0, 1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1, 0],
    [1, 2, 4, 3, 0, 5],
])
def test_merge_in_order_no_merge_method(orders):
    ndata = 6
    map_ = OrderedDict([(i, None) for i in range(ndata)])

    data = [MockDataWoMerge(name='data{}'.format(i)) for i in range(ndata)]

    for i in orders:
        merge_in_order(map_, i, data[i])

    assert [ ] == data[0].merged

##__________________________________________________________________||
