# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.binning import Round

##__________________________________________________________________||
def test_repr():
    obj = Round()
    repr(obj)

def test_call():
    obj = Round()
    assert 0.5 == obj(0.5)
    assert 0.5 == obj(1.4)
    assert 104.5 == obj(104.5)
    assert -0.5 == obj(-0.4)
    assert -0.5 == obj(-0.5)
    assert -1.5 == obj(-1.4)
    assert -1.5 == obj(-1.5)
    assert -2.5 == obj(-1.6)

def test_call_width_2():
    obj = Round(2)
    assert -3 == obj( -2.9)
    assert -3 == obj( -2  )
    assert -3 == obj( -1.1)
    assert -1 == obj( -0.9)
    assert -1 == obj(  0  )
    assert -1 == obj(  0.9)
    assert  1 == obj(  1.1)
    assert  1 == obj(  2  )
    assert  1 == obj(  2.9)

def test_call_width_2_aboundary_0():
    obj = Round(2, 0)
    assert -2 == obj( -1.9)
    assert -2 == obj( -1  )
    assert -2 == obj( -0.1)
    assert  0 == obj(  0.1)
    assert  0 == obj(  1  )
    assert  0 == obj(  1.9)
    assert  2 == obj(  2.1)
    assert  2 == obj(  3  )
    assert  2 == obj(  3.9)

def test_call_decimal_width():
    obj = Round(0.02, 0.005)
    assert  0.005 == pytest.approx(obj(  0.005))
    assert  0.025 == pytest.approx(obj(  0.025))
    assert  0.065 == pytest.approx(obj(  0.081))
    assert -0.055 == pytest.approx(obj( -0.048))
    assert -0.015 == pytest.approx(obj( -0.015))

def test_onBoundary():
    obj = Round()
    assert  -1.5 == obj( -1.5)
    assert  -0.5 == obj( -0.5)
    assert   0.5 == obj(  0.5)
    assert   1.5 == obj(  1.5)

    obj = Round(0.02, 0.005)
    assert  -0.035 == obj( -0.035)
    assert  -0.015 == obj( -0.015)
    assert   0.005 == obj(  0.005)
    assert   0.025 == obj(  0.025)
    assert   0.045 == obj(  0.045)

def test_next():
    obj = Round()
    assert  -0.5 == obj.next( -1.5)
    assert   0.5 == obj.next( -0.5)
    assert   1.5 == obj.next(  0.5)
    assert   2.5 == obj.next(  1.5)

    obj = Round(0.02, 0.005)
    assert  -0.015 == obj.next( -0.035)
    assert   0.005 == obj.next( -0.015)
    assert   0.025 == obj.next(  0.005)
    assert   0.045 == obj.next(  0.025)
    assert   0.065 == obj.next(  0.045)

def test_valid():
    obj = Round(valid=lambda x: x >= 0)
    assert   0.5 == obj(  1)
    assert  -0.5 == obj(  0)
    assert  None == obj( -1)

def test_min():
    obj = Round(10, 100, min=30)
    assert   100 == obj( 100)
    assert    30 == obj(  30)
    assert  None == obj(  29)

def test_min_underflow_bin():
    obj = Round(10, 100, min=30, underflow_bin=0)
    assert   100 == obj( 100)
    assert    30 == obj(  30)
    assert     0 == obj(  29)

    assert  obj(30) == obj.next( 0) # the next to the underflow
                                             # bin is the bin for the min

def test_max():
    obj = Round(10, 100, max=150)
    assert   100 == obj( 100)
    assert  None == obj( 150)
    assert  None == obj( 500)

    assert  None == obj.next(140) # the next to the last bin is
                                           # the overflow bin

def test_max_overflow_bin():
    obj = Round(10, 100, max=150, overflow_bin=150)
    assert   100 == obj( 100)
    assert   140 == obj( 149) # the last bin
    assert   150 == obj( 150) # overflow
    assert   150 == obj( 500) # overflow

    assert  150 == obj.next(140) # the next to the last
                                          # bin is the overflow
                                          # bin

    assert  150 == obj.next(150) # the next to the overflow
                                          # bin is the overflow bin

def test_max_overflow_bin_999():
    obj = Round(10, 100, max=150, overflow_bin=999)
    assert   100 == obj( 100)
    assert   140 == obj( 149) # the last bin
    assert   999 == obj( 150) # overflow
    assert   999 == obj( 500) # overflow

    assert  999 == obj.next(140) # the next to the last
                                          # bin is the overflow
                                          # bin

    assert  999 == obj.next(999) # the next to the overflow
                                          # bin is the overflow bin

def test_inf():
    obj = Round(10, 100)
    assert obj(float('inf')) is None
    assert obj(float('-inf')) is None
    assert obj.next(float('inf')) is None
    assert obj.next(float('-inf')) is None

##__________________________________________________________________||
