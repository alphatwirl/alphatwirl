# Tai Sakuma <tai.sakuma@gmail.com>
import copy
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
@pytest.fixture()
def tree():
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

    return dict(
        alls=(all0, all1, all2, all3),
        anys=(any1, ),
        nots=(not1, ),
        sels=(sel1, sel2, sel3, sel4, sel5)
    )

##__________________________________________________________________||
def test_combination(tree):

    all0 = tree['alls'][0]
    sels = tree['sels']

    event = mock.Mock()
    all0.begin(event)

    all_possible_results = itertools.product(*[[True, False]]*len(sels))
    # e.g.,
    # [
    #     (True, True, True, True, True),
    #     (True, True, True, True, False),
    #     ...
    #     (False, False, False, False, False)
    # ]

    for l in all_possible_results:
        # e.g. l = (True, True, False, True, False)
        for sel, ret in zip(sels, l):
            sel.return_value = ret
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
def test_merge():

    # manually call the fixture because multiple instances are needed

    # deep.copy() is not used because it will be difficult to access
    # to copied sels

    tree0 = tree()
    all0 = tree0['alls'][0]

    tree0_copy1 = tree()
    tree0_copy2 = tree()

    all0_copy1 = tree0_copy1['alls'][0]
    all0_copy2 = tree0_copy2['alls'][0]

    sels_copy1 = tree0_copy1['sels']
    sels_copy2 = tree0_copy2['sels']

    event = mock.Mock()
    all0_copy1.begin(event)
    all0_copy2.begin(event)

    all_possible_results = list(itertools.product(*[[True, False]]*len(sels_copy1)))

    results1 = all_possible_results[:len(all_possible_results)//2]
    results2 = all_possible_results[len(all_possible_results)//2:]

    for l in results1:
        for sel, ret in zip(sels_copy1, l):
            sel.return_value = ret
        all0_copy1(event)

    for l in results2:
        for sel, ret in zip(sels_copy2, l):
            sel.return_value = ret
        all0_copy2(event)

    all0_copy1.end()
    all0_copy2.end()

    all0.merge(all0_copy1)
    all0.merge(all0_copy2)

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
