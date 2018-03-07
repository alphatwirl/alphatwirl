# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.loop.splitfuncs import _apply_max_events_total

##__________________________________________________________________||
@pytest.mark.parametrize('args, expected', [
    pytest.param(
        ([('A', 100), ('B', 100)], 120),
        [('A', 100), ('B', 20)],
        id='simple'
    ),
    pytest.param(
        ([('A', 100), ('B', 200)], 300),
        [('A', 100), ('B', 200)],
        id='exact'
    ),
    pytest.param(
        ([('A', 100), ('B', 200)], 0),
        [ ],
        id='zero'
    ),
    pytest.param(
        ([ ], 10),
        [ ],
        id='empty'
    ),
])
def test_apply_max_events_total(args, expected):
    assert expected == _apply_max_events_total(*args)

##__________________________________________________________________||
