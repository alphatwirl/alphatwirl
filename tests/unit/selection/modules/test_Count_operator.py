# Tai Sakuma <tai.sakuma@gmail.com>
import copy
import logging
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules.Count import Count

##__________________________________________________________________||
@pytest.fixture()
def obj1_results_org():
    return [
        [1, 'class1', 'name1', 2, 2],
        [1, 'class1', 'name2', 1, 2],
        [1, 'class2', 'name3', 0, 1],
    ]

@pytest.fixture()
def obj1(obj1_results_org):
    ret = Count()
    ret._results = copy.deepcopy(obj1_results_org)
    return ret

@pytest.fixture()
def obj2_results_org():
    return [
        [1, 'class1', 'name1', 3, 5],
        [1, 'class1', 'name2', 2, 4],
        [1, 'class2', 'name3', 1, 2],
    ]

@pytest.fixture()
def obj2(obj2_results_org):
    ret = Count()
    ret._results = copy.deepcopy(obj2_results_org)
    return ret

@pytest.fixture()
def expected():
    return [
        [1, 'class1', 'name1', 5, 7],
        [1, 'class1', 'name2', 3, 6],
        [1, 'class2', 'name3', 1, 3],
    ]

def test_add(obj1, obj2, obj1_results_org, obj2_results_org, expected):
    obj3 = obj1 + obj2
    assert expected == obj3._results
    assert obj1._results is not obj3._results
    assert obj2._results is not obj3._results

    assert obj1_results_org is not obj1._results
    assert obj1_results_org == obj1._results

    assert obj2_results_org is not obj2._results
    assert obj2_results_org == obj2._results

def test_radd(obj1, obj2, obj1_results_org, obj2_results_org, expected):
    obj3 = sum([obj1, obj2]) # 0 + obj1 is executed
    assert expected == obj3._results
    assert obj1._results is not obj3._results
    assert obj2._results is not obj3._results

    assert obj1_results_org is not obj1._results
    assert obj1_results_org == obj1._results

    assert obj2_results_org is not obj2._results
    assert obj2_results_org == obj2._results

def test_iadd(obj1, obj2, obj1_results_org, obj2_results_org, expected):
    obj3 = obj1
    obj3 += obj2

    assert obj3 is obj1
    assert expected == obj3._results

    assert obj1_results_org is not obj1._results

    assert obj2_results_org is not obj2._results
    assert obj2_results_org == obj2._results

##__________________________________________________________________||
def test_add_incompatible_different_length(obj1, caplog):
    obj2 = Count()
    obj2._results  = [
        [1, 'class1', 'name1', 3, 5],
        [1, 'class1', 'name2', 2, 4],
    ]

    with caplog.at_level(logging.WARNING):
        obj3 = obj1 + obj2

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'Count' in caplog.records[0].name
    assert 'cannot add' in caplog.records[0].msg

    assert obj1._results == obj3._results

def test_add_incompatible_different_first_values(obj1, caplog):
    obj2 = Count()
    obj2._results  = [
        [1, 'class1', 'name1', 3, 5],
        [1, 'class1', 'name2', 2, 4],
        [1, 'class2', 'name4', 1, 2],
    ]

    with caplog.at_level(logging.WARNING):
        obj3 = obj1 + obj2

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'Count' in caplog.records[0].name
    assert 'cannot add' in caplog.records[0].msg

    obj3 = obj1 + obj2
    assert obj1._results == obj3._results

##__________________________________________________________________||
