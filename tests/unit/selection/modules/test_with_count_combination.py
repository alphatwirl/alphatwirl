# Tai Sakuma <tai.sakuma@gmail.com>
import itertools
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import AllwCount, AnywCount, NotwCount

##__________________________________________________________________||
class MockEventSelection(object):
    def begin(self, event): pass
    def __call__(self, event): pass
    def end(self): pass

##__________________________________________________________________||
def test_combination():
    # all0 - all1 --- all2 --- sel1
    #              |        +- sel2
    #              +- not1 --- any1 --- all3 --- sel3
    #                                |        +- sel4
    #                                +- sel5

    sel1 = mock.Mock(spec=MockEventSelection)
    sel1.name ='sel1'
    sel2 = mock.Mock(spec=MockEventSelection)
    sel2.name ='sel2'
    sel3 = mock.Mock(spec=MockEventSelection)
    sel3.name ='sel3'
    sel4 = mock.Mock(spec=MockEventSelection)
    sel4.name ='sel4'
    sel5 = mock.Mock(spec=MockEventSelection)
    sel5.name ='sel5'

    all0 = AllwCount(name='all0')
    all1 = AllwCount(name='all1')
    all2 = AllwCount(name='all2')
    all3 = AllwCount(name='all3')
    any1 = AnywCount(name='any1')

    all3.add(sel3)
    all3.add(sel4)
    any1.add(all3)
    any1.add(sel5)

    not1 = NotwCount(any1, name='not1')

    all2.add(sel1)
    all2.add(sel2)

    all1.add(all2)
    all1.add(not1)

    all0.add(all1)

    event = mock.Mock()
    all0.begin(event)

    for l in itertools.product(*[[True, False]]*5):
        sel1.return_value = l[0]
        sel2.return_value = l[1]
        sel3.return_value = l[2]
        sel4.return_value = l[3]
        sel5.return_value = l[4]
        all0(event)

    all0.end()

    count = all0.results()
    assert [
        [1,          'AllwCount', 'all1',  3, 32],
        [2,          'AllwCount', 'all2',  8, 32],
        [3, 'MockEventSelection', 'sel1', 16, 32],
        [3, 'MockEventSelection', 'sel2',  8, 16],
        [2 ,         'NotwCount', 'not1',  3,  8],
        [3,          'AnywCount', 'any1',  5,  8],
        [4,          'AllwCount', 'all3',  2,  8],
        [5, 'MockEventSelection', 'sel3',  4,  8],
        [5, 'MockEventSelection', 'sel4',  2,  4],
        [4, 'MockEventSelection', 'sel5',  3,  6]
    ] == count._results

##__________________________________________________________________||
