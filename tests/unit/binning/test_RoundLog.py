# Tai Sakuma <tai.sakuma@gmail.com>
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

def test_zero():
    obj = RoundLog()
    assert 0 == obj(0)

    assert 0 == obj.next(0) # next to 0 is 0 unless 0 is the
                            # underflow bin

def test_negative():
    obj = RoundLog()
    assert obj(-1) is None

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
    obj = RoundLog(0.1, 100, max=1000)
    assert 100 == obj(100)
    assert obj(1000) is None
    assert obj(5000) is None

def test_max_overflow_bin():
    obj = RoundLog(0.1, 100, max=1000, overflow_bin=1000)
    assert 100 == obj(100)
    assert 1000 == obj(1000)
    assert 1000 == obj(5000)

    assert 1000 == obj.next(1000) # the next to the overflow bin
                                  # is the overflow bin

def test_inf():
    obj = RoundLog(0.1, 100)
    assert obj(float('inf')) is None
    assert obj(float('-inf')) is None
    assert obj.next(float('inf')) is None
    assert obj.next(float('-inf')) is None

##__________________________________________________________________||
