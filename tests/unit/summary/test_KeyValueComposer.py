# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import math
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.summary import KeyValueComposer

##__________________________________________________________________||
class MockEvent(object):
    pass

class MockBinningEcho(object):
    def __call__(self, val):
        return val

class MockBinningFloor(object):
    def __init__(self, max=None):
        self.max = max

    def __call__(self, val):
        if val is None:
            return None
        if self.max is not None and not val <= self.max:
            return None
        return int(math.floor(val))

##__________________________________________________________________||
class MockArrayReader(object):
    def __init__(self, arrays=None, idxs_conf=None, backref_idxs=None):
        self.ret = ( )
        pass

    def read(self):
        return self.ret

class MockArrayReaderRaise(object):
    def __init__(self, arrays=None, idxs_conf=None, backref_idxs=None):
        pass

    def read(self):
        raise Exception('raised by MockArrayReaderRaise')

##__________________________________________________________________||
def test_repr():
    obj = KeyValueComposer()
    repr(obj)

##__________________________________________________________________||
def test_init_raise_wrong_key_length():
    with pytest.raises(ValueError):
        KeyValueComposer(
            keyAttrNames=('var1', ),
            keyIndices=(0, 1)
        )

def test_init_raise_wrong_val_length():
    with pytest.raises(ValueError):
        KeyValueComposer(
            valAttrNames = ('var1', ),
            valIndices = (0, 1)
        )

def test_init_raise_wrong_binning_length():
    with pytest.raises(ValueError):
        KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), MockBinningEcho()),
        )

##__________________________________________________________________||
def test_collect_arrays():
    obj = KeyValueComposer()

    event = MockEvent()
    event.var1 = [ ]
    event.var2 = [ ]
    event.var3 = [ ]
    attr_names = ('var1', 'var2', 'var3')
    arrays = obj._collect_arrays(event, attr_names)
    assert event.var1 is arrays[0]
    assert event.var2 is arrays[1]
    assert event.var3 is arrays[2]

def test_collect_arrays_error(caplog):
    obj = KeyValueComposer()

    event = MockEvent()
    event.var1 = [ ]
    event.var2 = [ ]
    attr_names = ('var1', 'var2', 'var3') # var3 doesn't exist

    with caplog.at_level(logging.WARNING):
        arrays = obj._collect_arrays(event, attr_names)

    assert arrays is None

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'KeyValueComposer' in caplog.records[0].name
    assert 'has no attribute' in caplog.records[0].msg

##__________________________________________________________________||
def test_call_inactive():
    obj = KeyValueComposer()
    obj.ArrayReader = MockArrayReader
    obj.active = False

    event = MockEvent()
    assert () == obj(event)

def test_call_raise():
    obj = KeyValueComposer()
    obj.active = True

    array_reader = MockArrayReaderRaise()
    obj._array_reader = array_reader

    event = MockEvent()
    with pytest.raises(Exception):
        obj(event)

##__________________________________________________________________||
def test_call_NoneKey_NoneVal():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 0
    obj.binnings = None

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((), )
    assert (((), ()), ) == obj(event)

def test_call_1Key_NoneVal():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 1
    obj.binnings = (MockBinningFloor(max=30), )

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((12.5, ), )
    assert (
        ((12,), ()),
    ) == obj(event)

    array_reader.ret = ((32.5, ), ) # out of range
    assert ( ) == obj(event)

def test_call_NoneKey_1Val():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 0
    obj.binnings = None

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((12.8, ), )
    assert (
        ((), (12.8, )),
    ) == obj(event)

def test_call_1Key_1Val():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 1
    obj.binnings = (MockBinningFloor(max=30), )

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((12.5, 20.3), )
    assert (
        ((12, ), (20.3, )),
    ) == obj(event)

    array_reader.ret = ((32.5, 20.3), )
    assert () == obj(event)

def test_call_2Keys_NoneVal():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 2
    obj.binnings = (MockBinningFloor(max=30), MockBinningFloor(max=50))

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((15.3, 22.8), )
    assert (
        ((15, 22), ()),
    ) == obj(event)

    array_reader.ret = ((45.3, 22.8), ) # 1st element out of range
    assert () == obj(event)

    array_reader.ret = ((15.3, 52.8), ) # 2nd element out of range
    assert () == obj(event)

    array_reader.ret = ((45.3, 52.8), ) # both out of range
    assert () == obj(event)

def test_call_2Keys_1Val():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 2
    obj.binnings = (MockBinningFloor(max=30), MockBinningFloor(max=50))

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((15.3, 22.8, 101.1), )
    assert (
        ((15, 22), (101.1, )),
    ) == obj(event)

    array_reader.ret = ((45.3, 22.8, 101.1), ) # 1st element out of range
    assert () == obj(event)

    array_reader.ret = ((15.3, 52.8, 101.1), ) # 2nd element out of range
    assert () == obj(event)

    array_reader.ret = ((45.3, 52.8, 101.1), ) # both out of range
    assert () == obj(event)

def test_call_2Keys_1Val_NoneBinnings():
    obj = KeyValueComposer()
    obj.active = True

    obj._lenkey = 2
    obj.binnings = None

    array_reader = MockArrayReader()
    obj._array_reader = array_reader

    event = MockEvent()

    array_reader.ret = ((15.3, 22.8, 101.1), )
    assert (
        ((15.3, 22.8), (101.1, )),
    ) == obj(event)

##__________________________________________________________________||
def test_example_back_reference_twice():
    obj = KeyValueComposer(
        keyAttrNames=('ev', 'jet_pt', 'jet_eta', 'mu_pt', 'mu_eta', 'jet_phi'),
        binnings=(
            MockBinningFloor(),
            MockBinningFloor(),
            MockBinningFloor(max=3), # <- use max for jet_eta
            MockBinningFloor(),
            MockBinningFloor(max=2), # <- use max for mu_eta
            MockBinningEcho(),
        ),
        keyIndices=(None, '(*)', '\\1', '(*)', '\\2', '\\1'),
        valAttrNames=('jet_energy', 'muon_energy'),
        valIndices=('\\1', '\\2'),
    )

    event = MockEvent()
    event.ev = [ ]
    event.jet_pt = [ ]
    event.jet_eta = [ ]
    event.jet_phi = [ ]
    event.jet_energy = [ ]
    event.mu_pt = [ ]
    event.mu_eta = [ ]
    event.muon_energy = [ ]
    obj.begin(event)

    event.ev[:] = [1001]
    event.jet_pt[:]  =    [ 15.3, 12.9,  9.2, 10.5]
    event.jet_eta[:] =    [ -1.2,  5.2,  2.2,  0.5] # <- 2nd value is greater than max
    event.jet_phi[:] =    [  0.1,  0.6,  1.2] # <- the last value is missing
    event.jet_energy[:] = [ 16.2, 13.1, 10.1, 11.8]
    event.mu_pt[:]  =      [ 20.2, 11.9, 13.3,  5.2]
    event.mu_eta[:] =      [ 2.2,   1.2, -1.5, -0.5] # <- 1st value is greater than max
    event.muon_energy[:] = [ 22.1, 15.2, 16.3] # <- the last value is missing

    assert (
        ((1001, 15, -2, 11,  1, 0.1), (16.2, 15.2)),
        ((1001, 15, -2, 13, -2, 0.1), (16.2, 16.3)),
        ((1001,  9,  2, 11,  1, 1.2), (10.1, 15.2)),
        ((1001,  9,  2, 13, -2, 1.2), (10.1, 16.3)),
    ) == obj(event)

##__________________________________________________________________||
