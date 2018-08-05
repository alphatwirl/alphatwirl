# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from alphatwirl.binning import Binning

##__________________________________________________________________||
def test_repr():
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(boundaries=boundaries)
    repr(obj)

def test_call():
    bins = (1, 2, 3, 4)
    lows = (10.0, 20.0, 30.0, 40.0)
    ups = (20.0, 30.0, 40.0, 50.0)
    obj = Binning(bins=bins, lows=lows, ups=ups, retvalue='number')
    assert 1 == obj(15)
    assert 2 == obj(21)
    assert 2 == obj(20) # on the low edge
    assert 0 == obj(5) # underflow
    assert 5 == obj(55) # overflow

def test_onBoundary():
    boundaries = (0.000001, 0.00001, 0.0001)
    obj = Binning(boundaries=boundaries, retvalue='number')
    assert  1 == obj( 0.000001 )
    assert  2 == obj( 0.00001  )
    assert  3 == obj( 0.0001   )

def test_lowedge():
    lows = (10.0, 20.0, 30.0, 40.0)
    ups = (20.0, 30.0, 40.0, 50.0)
    obj = Binning(lows=lows, ups=ups, retvalue='lowedge')
    assert             10 == obj( 15 )
    assert             20 == obj( 21 )
    assert             20 == obj( 20 )
    assert  float("-inf") == obj(  5 )
    assert             50 == obj( 55 )

    obj = Binning(lows=lows, ups=ups) # 'lowedge' is default
    assert             10 == obj( 15 )
    assert             20 == obj( 21 )
    assert             20 == obj( 20 )
    assert  float("-inf") == obj(  5 )
    assert             50 == obj( 55 )

def test_init_retvalue():
    boundaries = (10, 20, 30, 40, 50)
    Binning(boundaries=boundaries)
    Binning(boundaries=boundaries, retvalue='number')
    Binning(boundaries=boundaries, retvalue='lowedge')
    with pytest.raises(ValueError):
        Binning(boundaries=boundaries, retvalue='center')

    with pytest.raises(ValueError):
        Binning(boundaries=boundaries, retvalue='yyy')

    with pytest.raises(ValueError):
        Binning(boundaries=boundaries, retvalue='lowedge', bins=(1, 2, 3, 4))

    with pytest.raises(ValueError):
        Binning(boundaries=boundaries, retvalue='lowedge', underflow_bin=-1)

    with pytest.raises(ValueError):
        Binning(boundaries=boundaries, retvalue='lowedge', overflow_bin=-1)

def test_init_with_bins_lows_ups():
    bins = (1, 2, 3, 4)
    lows = (10.0, 20.0, 30.0, 40.0)
    ups = (20.0, 30.0, 40.0, 50.0)
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(bins=bins, lows=lows, ups=ups, retvalue='number')
    assert bins == obj.bins
    assert boundaries == obj.boundaries

def test_init_with_lows_ups():
    bins = (1, 2, 3, 4)
    lows = (10.0, 20.0, 30.0, 40.0)
    ups = (20.0, 30.0, 40.0, 50.0)
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(lows=lows, ups=ups, retvalue='number')
    assert bins == obj.bins
    assert boundaries == obj.boundaries

def test_init_with_boundaries():
    bins = (1, 2, 3, 4)
    lows = (10.0, 20.0, 30.0, 40.0)
    ups = (20.0, 30.0, 40.0, 50.0)
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(boundaries=boundaries, retvalue='number')
    assert bins == obj.bins
    assert lows == obj.lows
    assert ups == obj.ups

def test_init_exceptions():
    with pytest.raises(ValueError):
        Binning()

    with pytest.raises(ValueError):
        Binning(lows=1)

    with pytest.raises(ValueError):
        Binning(ups=1)

    with pytest.raises(ValueError):
        Binning(boundaries=1, lows=1)

    with pytest.raises(ValueError):
        Binning(boundaries=1, ups=1)

    with pytest.raises(ValueError):
        Binning(boundaries=1, lows=1, ups=1)

    lows = (10.0, 20.0, 30.0, 45.0)
    ups = (20.0, 30.0, 40.0, 50.0)

    with pytest.raises(ValueError):
        Binning(lows=lows, ups=ups)

def test_init_exceptions_nobin():
    boundaries = (10, )

    with pytest.raises(ValueError):
        Binning(boundaries=boundaries)

def test_next_number():
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(boundaries=boundaries, retvalue='number')
    assert  1 == obj.next(0)
    assert  2 == obj.next(1)
    assert  3 == obj.next(2)
    assert  4 == obj.next(3)
    assert  5 == obj.next(4)
    assert  5 == obj.next(5)

    assert 5 == obj.next(5) # overflow_bin returns the same

    with pytest.raises(ValueError):
         obj.next(2.5)

    with pytest.raises(ValueError):
        obj.next(6)

def test_next_lowedge():
    boundaries = (10, 20, 30, 40, 50)
    obj = Binning(boundaries=boundaries, retvalue='lowedge')

    # on the boundaries
    assert  20 == obj.next(10)
    assert  30 == obj.next(20)
    assert  40 == obj.next(30)
    assert  50 == obj.next(40)
    assert  50 == obj.next(50)

    # underflow_bin
    assert 10 == obj.next(float('-inf'))

    boundaries = (0.001, 0.002, 0.003, 0.004, 0.005)
    obj = Binning(boundaries=boundaries, retvalue='lowedge')
    assert  0.002 == obj.next( 0.001)
    assert  0.003 == obj.next( 0.002)
    assert  0.004 == obj.next( 0.003)
    assert  0.005 == obj.next( 0.004)
    assert  0.005 == obj.next( 0.005)

def test_valid():
    obj = Binning(boundaries=(30, 40, 50), retvalue='number', valid=lambda x: x >= 10)
    assert  1 == obj( 33)
    assert  2 == obj( 45)
    assert obj( 9) is None

##__________________________________________________________________||
