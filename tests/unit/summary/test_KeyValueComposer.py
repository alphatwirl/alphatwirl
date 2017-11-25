import unittest
import logging
import math

import alphatwirl.summary as summary

##__________________________________________________________________||
class MockEvent(object):
    pass

##__________________________________________________________________||
class MockBinningEcho(object):
    def __call__(self, val):
        return val

##__________________________________________________________________||
class MockBinningFloor(object):
    def __init__(self, max = None):
        self.max = max

    def __call__(self, val):
        if val is None: return None
        if self.max is not None and not val <= self.max: return None
        return int(math.floor(val))

##__________________________________________________________________||
class MockArrayReader(object):
    def __init__(self, arrays = None, idxs_conf = None, backref_idxs = None):
        self.ret = ( )
        pass

    def read(self):
        return self.ret

##__________________________________________________________________||
class MockArrayReaderRaise(object):
    def __init__(self, arrays = None, idxs_conf = None, backref_idxs = None):
        pass

    def read(self):
        raise Exception('raised by MockArrayReaderRaise')

##__________________________________________________________________||
class TestKeyValueComposer(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_repr(self):
        obj = summary.KeyValueComposer()
        repr(obj)

    def test_init_raise_wrong_key_length(self):
        self.assertRaises(
            ValueError,
            summary.KeyValueComposer,
            keyAttrNames = ('var1', ),
            keyIndices = (0, 1)
            )

    def test_init_raise_wrong_val_length(self):
        self.assertRaises(
            ValueError,
            summary.KeyValueComposer,
            valAttrNames = ('var1', ),
            valIndices = (0, 1)
            )

    def test_init_raise_wrong_binning_length(self):
        self.assertRaises(
            ValueError,
            summary.KeyValueComposer,
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), MockBinningEcho()),
            )

    def test_collect_arrays(self):
        obj = summary.KeyValueComposer()

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        attr_names = ('var1', 'var2', 'var3')
        arrays = obj._collect_arrays(event, attr_names)
        self.assertIs(event.var1, arrays[0])
        self.assertIs(event.var2, arrays[1])
        self.assertIs(event.var3, arrays[2])

    def test_collect_arrays_error(self):
        obj = summary.KeyValueComposer()

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        attr_names = ('var1', 'var2', 'var3') # var3 doesn't exist
        arrays = obj._collect_arrays(event, attr_names)
        self.assertIsNone(arrays)

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_logging_nonexistent_var(self):
        obj = summary.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            valAttrNames = ('var2', ),
        )

        event = MockEvent()
        event.var2 = [ ]
        obj.begin(event)

        event.var2[:] = [20.3, ]
        self.assertEqual(( ), obj(event))

    def test_call_inactive(self):
        obj = summary.KeyValueComposer()
        obj.ArrayReader = MockArrayReader
        obj.active = False

        event = MockEvent()
        self.assertEqual((), obj(event))

    def test_call_raise(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        array_reader = MockArrayReaderRaise()
        obj._array_reader = array_reader

        event = MockEvent()
        self.assertRaises(Exception, obj, event)

    def test_call_NoneKey_NoneVal(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 0
        obj.binnings = None

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((), )
        self.assertEqual(
            (
                ((), ()),
            ), obj(event))

    def test_call_1Key_NoneVal(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 1
        obj.binnings = (MockBinningFloor(max = 30), )

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((12.5, ), )
        self.assertEqual(
            (
                ((12,), ()),
            ), obj(event))

        array_reader.ret = ((32.5, ), ) # out of range
        self.assertEqual((), obj(event))

    def test_call_NoneKey_1Val(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 0
        obj.binnings = None

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((12.8, ), )
        self.assertEqual(
            (
                ((), (12.8, )),
            ), obj(event))

    def test_call_1Key_1Val(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 1
        obj.binnings = (MockBinningFloor(max = 30), )

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((12.5, 20.3), )
        self.assertEqual(
            (
                ((12, ), (20.3, )),
            ), obj(event))

        array_reader.ret = ((32.5, 20.3), )
        self.assertEqual((), obj(event))

    def test_call_2Keys_NoneVal(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 2
        obj.binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50))

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((15.3, 22.8), )
        self.assertEqual(
            (
                ((15, 22), ()),
            ), obj(event))

        array_reader.ret = ((45.3, 22.8), ) # 1st element out of range
        self.assertEqual((), obj(event))

        array_reader.ret = ((15.3, 52.8), ) # 2nd element out of range
        self.assertEqual((), obj(event))

        array_reader.ret = ((45.3, 52.8), ) # both out of range
        self.assertEqual((), obj(event))

    def test_call_2Keys_1Val(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 2
        obj.binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50))

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((15.3, 22.8, 101.1), )
        self.assertEqual(
            (
                ((15, 22), (101.1, )),
            ), obj(event))

        array_reader.ret = ((45.3, 22.8, 101.1), ) # 1st element out of range
        self.assertEqual((), obj(event))

        array_reader.ret = ((15.3, 52.8, 101.1), ) # 2nd element out of range
        self.assertEqual((), obj(event))

        array_reader.ret = ((45.3, 52.8, 101.1), ) # both out of range
        self.assertEqual((), obj(event))

    def test_call_2Keys_1Val_NoneBinnings(self):
        obj = summary.KeyValueComposer()
        obj.active = True

        obj._lenkey = 2
        obj.binnings = None

        array_reader = MockArrayReader()
        obj._array_reader = array_reader

        event = MockEvent()

        array_reader.ret = ((15.3, 22.8, 101.1), )
        self.assertEqual(
            (
                ((15.3, 22.8), (101.1, )),
            ), obj(event))

    def test_example_back_reference_twice(self):
        obj = summary.KeyValueComposer(
            keyAttrNames = ('ev', 'jet_pt', 'jet_eta', 'mu_pt', 'mu_eta', 'jet_phi'),
            binnings = (
                MockBinningFloor(),
                MockBinningFloor(),
                MockBinningFloor(max = 3), # <- use max for jet_eta
                MockBinningFloor(),
                MockBinningFloor(max = 2), # <- use max for mu_eta
                MockBinningEcho(),
            ),
            keyIndices = (None, '(*)', '\\1', '(*)', '\\2', '\\1'),
            valAttrNames = ('jet_energy', 'muon_energy'),
            valIndices = ('\\1', '\\2'),
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

        self.assertEqual(
            (
                ((1001, 15, -2, 11,  1, 0.1), (16.2, 15.2)),
                ((1001, 15, -2, 13, -2, 0.1), (16.2, 16.3)),
                ((1001,  9,  2, 11,  1, 1.2), (10.1, 15.2)),
                ((1001,  9,  2, 13, -2, 1.2), (10.1, 16.3)),
            ),
            obj(event)
        )

##__________________________________________________________________||
