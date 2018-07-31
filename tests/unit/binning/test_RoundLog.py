# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.binning import RoundLog

##__________________________________________________________________||
def test_repr():
    obj = RoundLog()
    repr(obj)

def test_call():
    obj = RoundLog()
    assert 1.9952623149688 == pytest.approx(obj(   2))
    assert 19.952623149688 == pytest.approx(obj(  20))
    assert 199.52623149688 == pytest.approx(obj( 200))

def test_next():
    obj = RoundLog()
    assert 2.51188643150958 == pytest.approx(obj.next(2.23872113856834))
    assert 25.11886431509581 == pytest.approx(obj.next(22.3872113856834))
    assert 251.18864315095848 == pytest.approx(obj.next(223.872113856834))

def test_call_zero():
    obj = RoundLog()
    assert 0 == obj(0)

    assert 0 == obj.next(0) # next to 0 is 0 unless 0 is the
                            # underflow bin

def test_call_negative():
    obj = RoundLog()
    assert obj(-1) is None

def test_valid():
    obj = RoundLog(valid=lambda x: x >= 10)
    assert 12.589254117941675 == pytest.approx(obj(13))
    assert 10.0 == pytest.approx(obj(10))
    assert obj(7) is None

def test_onBoundary():
    obj = RoundLog(0.1, 100)
    assert 100 == obj(100)
#
def test_min():
    obj = RoundLog(0.1, 100, min=10)
    assert 100 == obj(100)
    assert 10 == pytest.approx(obj(  10))
    assert obj(9) is None

def test_min_underflow_bin():
    obj = RoundLog(0.1, 100, min=10, underflow_bin=0)
    assert 100 == obj(100)
    assert 10 == pytest.approx(obj(10))
    assert 0 == obj(   9)

    assert obj(10) == obj.next(0) # the next to the underflow
                                   # bin is the bin for the min

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
