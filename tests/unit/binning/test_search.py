# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.binning.search import linear_search, binary_search

##__________________________________________________________________||
@pytest.mark.parametrize('search', [linear_search, binary_search])
@pytest.mark.parametrize('val, boundaries, expected', [
    pytest.param(0.1, [0.1], 0, id='one-boundary'),
    pytest.param(0.1, [0.1, 0.2], 0, id='two-boundaries-at-lowedge'),
    pytest.param(0.15, [0.1, 0.2], 0, id='two-boundaries-in-bin'),
    pytest.param(0.2, [0.1, 0.2], 1, id='two-boundaries-at-upedge'),
    pytest.param(0.1, [0.1, 0.2, 0.3], 0, id='three-boundaries'),
    pytest.param(0.15, [0.1, 0.2, 0.3], 0, id='three-boundaries'),
    pytest.param(0.2, [0.1, 0.2, 0.3], 1, id='three-boundaries'),
    pytest.param(0.25, [0.1, 0.2, 0.3], 1, id='three-boundaries'),
    pytest.param(0.3, [0.1, 0.2, 0.3], 2, id='three-boundaries'),
    pytest.param(0.1, [0.1, 0.2, 0.3, 0.4], 0, id='four-boundaries'),
    pytest.param(0.15, [0.1, 0.2, 0.3, 0.4], 0, id='four-boundaries'),
    pytest.param(0.2, [0.1, 0.2, 0.3, 0.4], 1, id='four-boundaries'),
    pytest.param(0.25, [0.1, 0.2, 0.3, 0.4], 1, id='four-boundaries'),
    pytest.param(0.3, [0.1, 0.2, 0.3, 0.4], 2, id='four-boundaries'),
    pytest.param(0.35, [0.1, 0.2, 0.3, 0.4], 2, id='four-boundaries'),
    pytest.param(0.4, [0.1, 0.2, 0.3, 0.4], 3, id='four-boundaries'),
])
def test_search(search, val, boundaries, expected):
    assert expected == search(val, boundaries)

##__________________________________________________________________||
