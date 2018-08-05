# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np
import functools
import pytest

from alphatwirl.binning import RoundLog

##__________________________________________________________________||
def test_repr():
    obj = RoundLog()
    repr(obj)

def test_default():
    obj = RoundLog()
    assert 1.9952623149688 == pytest.approx(obj(   2))
    assert 19.952623149688 == pytest.approx(obj(  20))
    assert 199.52623149688 == pytest.approx(obj( 200))

def test_next():
    obj = RoundLog()
    assert 2.51188643150958 == pytest.approx(obj.next(2.23872113856834))
    assert 25.11886431509581 == pytest.approx(obj.next(22.3872113856834))
    assert 251.18864315095848 == pytest.approx(obj.next(223.872113856834))

@pytest.mark.parametrize('min_', [None, 10])
@pytest.mark.parametrize('underflow_bin', [None, -1, 0, 0.001])
def test_zero(min_, underflow_bin):
    obj = RoundLog(0.1, 100, min_, underflow_bin)
    if min_ is None:
        assert 0 == obj(0)
        assert 0 == obj(-0)
        assert 0 == obj(0.0)
        assert 0 == obj(-0.0)
    else:
        assert obj(0) is underflow_bin
        assert obj(-0) is underflow_bin
        assert obj(0.0) is underflow_bin
        assert obj(-0.0) is underflow_bin

    if min_ is None:
        assert 0 == obj.next(0) # next to 0 is 0 unless 0 is the
                                # underflow bin
    else:
        if underflow_bin is None:
            assert obj.next(underflow_bin) is None
        else:
            assert obj(min_) == obj.next(underflow_bin)
            # the next to the underflow bin is the bin for the min

@pytest.mark.parametrize('min_', [None, 10])
@pytest.mark.parametrize('underflow_bin', [None, -1, 0, 0.001])
def test_negative(min_, underflow_bin):
    obj = RoundLog(0.1, 100, min_, underflow_bin)
    if min_ is None:
        assert obj(-2.1) is None
        assert obj(float('-inf')) is None
    else:
        assert obj(-2.1) is underflow_bin
        assert obj(float('-inf')) is underflow_bin

def test_valid():
    obj = RoundLog(valid=lambda x: x >= 10)
    assert 12.589254117941675 == pytest.approx(obj(13))
    assert 10.0 == pytest.approx(obj(10))
    assert obj(7) is None

def test_on_boundary():
    obj = RoundLog(0.1, 100)
    assert 100 == obj(100)

@pytest.mark.parametrize('width', [0.1, 0.2])
@pytest.mark.parametrize('underflow_bin', [None, -1, 0, 0.001])
def test_min_on_a_boundary(width, underflow_bin):
    # this test is related to
    # the issue 43
    # https://github.com/alphatwirl/alphatwirl/issues/43

    min_ = 10 # on a boundary
    obj = RoundLog(width, 100, min=min_, underflow_bin=underflow_bin)

    # boundaries (on a computer)
    # when width = 0.1:
    #   [10.00, 12.59, 15.85, 19.95, 25.12, 31.62,
    #    39.81, 50.12, 63.10, 79.43, 100.00]
    #   10.00 is actually 9.999999999999982, so is the first bin
    #
    # when width = 0.2:
    #   [6.31, 10.00, 15.85, 25.12, 39.81, 63.10, 100.00']
    #   10.00 here actually is 10.000000000000005, so is the 2nd bin

    assert 100 == obj(100)
    # 100 is exact because it is the given boundary

    # min_=10 is a boundary, but not necessarily exact.
    if min_ == pytest.approx(obj(min_)):
        # when width = 0.1 (in the above example)
        assert obj(11) == obj(min_)
        assert obj(9) is underflow_bin
    else:
        # when width = 0.2 (in the above example)
        assert obj(9) is not underflow_bin
        assert obj(9) == obj(min_)

    assert obj(6.3) is underflow_bin

    if underflow_bin is None:
        assert obj.next(underflow_bin) is None
    else:
        assert obj(min_) == obj.next(underflow_bin)
        # the next to the underflow bin is the bin for the min

def test_max():
    obj = RoundLog(0.1, 100, max=900)
    # max=900 is not a boundary

    assert 100 == obj(100)

    assert obj(900) is not None
    assert obj(1100) is None

@pytest.mark.parametrize('width', [0.1, 0.2])
@pytest.mark.parametrize('log10_max', [1.6, 2.4])
@pytest.mark.parametrize('overflow_bin', [None, True, 1000])
def test_max_float_on_a_boundary(width, log10_max, overflow_bin):

    max_ = 10**log10_max # max_ on a boundary (within rounding of float)
    obj = RoundLog(width, 10.0, max=max_, overflow_bin=overflow_bin)

    log10_boundaries = obj._round.boundaries

    if overflow_bin is True:
        overflow_bin = 10**log10_boundaries[-1]

    assert 10.0 == obj(10.0)
    # this is always true because it is the given boundary.

    # If the max is exactly a boundary, the max is the upper edge of
    # the last bin and bin(max) is overflow because the upper edge is
    # open. Otherwise, bin(max) is in the last bin.
    if log10_max == log10_boundaries[-1]:
        assert obj(max_) == overflow_bin
    else:
        assert 10**log10_boundaries[-2] == obj(max_)

    # The max is either the upper or lower edge of the last bin, but
    # not necessarily exact.
    if not log10_max == pytest.approx(log10_boundaries[-1]):
        assert log10_max == pytest.approx(log10_boundaries[-2])

    # the next to the last bin is the overflow bin
    assert obj.next(10**log10_boundaries[-2]) == overflow_bin

    # the next to the overflow bin is the overflow bin
    assert obj.next(overflow_bin) == overflow_bin

@pytest.mark.parametrize('max_', [None, 1000])
@pytest.mark.parametrize('overflow_bin', [None, True, 1000])
def test_inf(max_, overflow_bin):
    obj = RoundLog(0.1, 10.0, max=max_, overflow_bin=overflow_bin)

    log10_boundaries = obj._round.boundaries
    if overflow_bin is True:
        overflow_bin = 10**log10_boundaries[-1]

    if max_ is None:
        assert obj(float('inf')) is None
        assert obj(float('-inf')) is None
        assert obj.next(float('inf')) is None
        assert obj.next(float('-inf')) is None
    else:
        assert obj(float('inf')) == overflow_bin
        assert obj(float('-inf')) is None

##__________________________________________________________________||
def to_be_benchmarked(obj):
    val = np.random.exponential(scale=100)
    obj(val)

@pytest.mark.skip(reason='for optimizing for speed')
def test_benchmark(benchmark):
    np.random.seed(0)
    obj = RoundLog(0.1, 100)
    benchmark(to_be_benchmarked, obj)

##__________________________________________________________________||
def to_be_profiled(obj, vals):
    for val in vals:
        obj(val)

@pytest.mark.skip(reason='for optimizing for speed')
def test_profile():
    np.random.seed(0)
    from alphatwirl.misc import profile_func
    obj = RoundLog(0.05, 100)
    vals = np.random.exponential(scale=100, size=500000)
    print(profile_func(functools.partial(to_be_profiled, obj, vals)))

##__________________________________________________________________||
