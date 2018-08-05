# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.binning.search import linear_search

##__________________________________________________________________||
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
])
def test_search(val, boundaries, expected):
    assert expected == linear_search(val, boundaries)
##__________________________________________________________________||
