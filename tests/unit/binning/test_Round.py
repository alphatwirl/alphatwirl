# Tai Sakuma <tai.sakuma@gmail.com>
import numbers
import pytest

from alphatwirl.binning import Round

##__________________________________________________________________||
def test_repr():
    obj = Round()
    repr(obj)

def test_default():
    obj = Round()
    assert 0.5 == obj(0.5)
    assert 0.5 == obj(1.4)
    assert 104.5 == obj(104.5)
    assert -0.5 == obj(-0.4)
    assert -0.5 == obj(-0.5)
    assert -1.5 == obj(-1.4)
    assert -1.5 == obj(-1.5)
    assert -2.5 == obj(-1.6)

def test_width_2():
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

def test_width_2_aboundary_0():
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

def test_decimal_width():
    obj = Round(0.02, 0.005)
    assert  0.005 == pytest.approx(obj(  0.005))
    assert  0.025 == pytest.approx(obj(  0.025))
    assert  0.065 == pytest.approx(obj(  0.081))
    assert -0.055 == pytest.approx(obj( -0.048))
    assert -0.015 == pytest.approx(obj( -0.015))

def test_keep_aboundary_int():
    # This test is to make sure boundaries are int
    # width/2 is int in both python 2 and 3
    # https://www.python.org/dev/peps/pep-0238/
    obj = Round(4)
    assert 2 == (obj(4))
    assert isinstance(obj(4), numbers.Integral)

def test_on_boundary():
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

def test_min_int():
    obj = Round(10, 100, min=30)
    assert   100 == obj( 100)
    assert    30 == obj(  30) # this works for int
    assert  None == obj(  29)

def test_min_float_not_a_boundary():
    obj = Round(0.2, 2.0, min=1.1)
    # boundaries = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    # min=1.1 is not a boundary

    assert 2.0 == obj(2.0)
    # this is always true because 2.0 is the given boundary.

    assert 1.0 == pytest.approx(obj(1.05))
    # 1.05 is below min=1.1. However, it is above the lower edge of
    # the bin 1.1 belongs, which is 1.0. So obj(1.05) should returns
    # the lower edge.

    assert obj(0.95) is None

@pytest.mark.parametrize('width', [0.1, 0.2])
@pytest.mark.parametrize('underflow_bin', [None, -1, 0, 0.1])
def test_min_on_a_boundary(width, underflow_bin):
    # this test is related to
    # the issue 43
    # https://github.com/alphatwirl/alphatwirl/issues/43

    min_ = 1.0 # on a boundary (within rounding of float)
    obj = Round(width, 2.0, min=min_, underflow_bin=underflow_bin)

    # example boundaries (depending on the architecture)
    # when width = 1.0:
    #     boundaries = [
    #         0.9999999999999992, 1.0999999999999992,
    #         1.1999999999999993, 1.2999999999999994, 1.3999999999999995,
    #         1.4999999999999996, 1.5999999999999996, 1.6999999999999997,
    #         1.7999999999999998, 1.9, 2.0]
    #   min=1.0 is the 1st element. but the precise value is slightly
    #   less than 1.0
    #
    # when width = 2.0:
    # boundaries = [
    #     0.8000000000000003, 1.0000000000000002,
    #     1.2000000000000002, 1.4000000000000001, 1.6, 1.8, 2.0]
    #   min=1.0 is the 2nd element, slightly greater than 1.0.

    assert 2.0 == obj(2.0)
    # this is always true because 2.0 is the given boundary.

    # min=1.0 is a boundary, but not necessarily exact.
    if min_ == pytest.approx(obj(min_)):
        assert obj(1.05) == obj(min_)
        assert obj(0.95) is underflow_bin
    else:
        assert obj(0.95) is not underflow_bin
        assert obj(0.95) == obj(min_) # in the same bin as min
    # the results depend on the architecture.
    # it is wise to not set min a boundary.

    assert obj(0.7) is underflow_bin

    if underflow_bin is None:
        assert obj.next(underflow_bin) is None
    else:
        assert obj(min_) == obj.next(underflow_bin)
        # the next to the underflow bin is the bin for the min

def test_max_int():
    obj = Round(10, 100, max=150)
    assert   100 == obj( 100)
    assert  None == obj( 150)
    assert  None == obj( 500)

    assert  None == obj.next(140) # the next to the last bin is
                                           # the overflow bin

def test_max_float():
    obj = Round(0.2, 2.0, max=2.5)
    # boundaries = [2.0, 2.2, 2.4, 2.6]
    # max=2.5 is not a boundary

    assert 2.0 == obj(2.0)
    # this is always true because 2.0 is the given boundary.

    assert 2.4 == pytest.approx(obj(2.5))
    assert 2.4 == pytest.approx(obj(2.55))

    assert obj(2.61) is None

def test_max_not_on_a_boundary_overflow_bin():
    obj = Round(10, 100, max=145, overflow_bin=150)
    assert   100 == obj( 100)
    assert   140 == obj( 149) # the last bin
    assert   150 == obj( 150) # overflow
    assert   150 == obj( 500) # overflow

    assert  150 == obj.next(140) # the next to the last
                                          # bin is the overflow
                                          # bin

    assert  150 == obj.next(150) # the next to the overflow
                                          # bin is the overflow bin

def test_max_on_a_boundary_overflow_bin():
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

def test_max_not_on_a_boundary_overflow_bin_true():
    obj = Round(10, 100, max=145, overflow_bin=True)
    print(obj.boundaries)
    assert   100 == obj( 100)
    assert   140 == obj( 149) # the last bin
    assert   150 == obj( 150) # overflow
    assert   150 == obj( 500) # overflow

    assert  150 == obj.next(140) # the next to the last
                                          # bin is the overflow
                                          # bin

    assert  150 == obj.next(150) # the next to the overflow
                                          # bin is the overflow bin

def test_max_on_a_boundary_overflow_bin_true():
    obj = Round(10, 100, max=150, overflow_bin=True)
    print(obj.boundaries)
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
