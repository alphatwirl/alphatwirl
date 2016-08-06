import AlphaTwirl.Counter as Counter
import unittest
import logging
import math

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
class TestKeyValueComposer_arguments(unittest.TestCase):

    def test_raise_1(self):
        self.assertRaises(
            ValueError,
            Counter.KeyValueComposer,
            binnings = (MockBinningEcho(), ),
            )

    def test_raise_2(self):
        self.assertRaises(
            ValueError,
            Counter.KeyValueComposer,
            valAttrNames = ('var1', ),
            valIndices = (0, 1)
            )

##__________________________________________________________________||
@unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
class TestKeyValueComposer_logging(unittest.TestCase):
    def test_empty_branch(self):
        keyComposer = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho())
        )

        event = MockEvent()
        event.var1 = [ ]
        keyComposer.begin(event)

        event.var1[:] = [15, ]
        self.assertEqual(( ), keyComposer(event))

##__________________________________________________________________||
class TestKeyValueComposer_simple(unittest.TestCase):

    def test_1Key_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            valAttrNames = ('var2', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, ]
        event.var2[:] = [20.3, ]
        self.assertEqual(
            (
                ((12, ), (20.3, )),
            ), obj(event))

        event.var1[:] = [32.5, ] # <- out of range
        event.var2[:] = [20.3, ]
        self.assertEqual(( ), obj(event))

    def test_1Key_1Val_mix_list_tuple(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ['var1', ], # <- list
            binnings = (MockBinningFloor(max = 30), ),
            valAttrNames = ('var2', ), # <- tuple
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, ]
        event.var2[:] = [20.3, ]
        self.assertEqual(
            (
                ((12, ), (20.3, )),
            ), obj(event))

        event.var1[:] = [32.5, ] # <- out of range
        event.var2[:] = [20.3, ]
        self.assertEqual(( ), obj(event))

    def test_1Key_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            valAttrNames = None, # <- None
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, ]
        self.assertEqual(
            (
                ((12, ), ( )),
            ), obj(event))

        event.var1[:] = [32.5, ] # out of range
        self.assertEqual(( ), obj(event))

    def test_1Key_emptyVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            valAttrNames = (), # <- empty
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, ]
        self.assertEqual(
            (
                ((12, ), ( )),
            ), obj(event))

        event.var1[:] = [32.5, ] # out of range
        self.assertEqual(( ), obj(event))

    def test_NoneKey_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = None, # <- None
            valAttrNames = ('var1', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.8, ]
        self.assertEqual(
            (
                (( ), (12.8, )),
            ), obj(event))

    def test_emptyKey_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = (), # <- empty
            valAttrNames = ('var1', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.8, ]
        self.assertEqual(
            (
                (( ), (12.8, )),
            ), obj(event))

    def test_NoneKey_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = None,
            valAttrNames = None,
        )

        event = MockEvent()
        obj.begin(event)

        self.assertEqual(
            (
                (( ), ( )),
            ), obj(event))

    def test_2Keys_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50))
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [15.3, ]
        event.var2[:] = [22.8, ]
        self.assertEqual(
            (
                ((15, 22), ( )),
            ), obj(event))

        event.var1[:] = [45.3, ] # <- out of range
        event.var2[:] = [22.8, ]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [45.3, ]
        event.var2[:] = [52.8, ] # <- out of range
        self.assertEqual(( ), obj(event))

    def test_2Keys_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50)),
            valAttrNames = ('var3', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        obj.begin(event)

        event.var1[:] = [15.2, ]
        event.var2[:] = [22.8, ]
        event.var3[:] = [101.1, ]
        self.assertEqual(
            (
                ((15, 22), (101.1, )),
            ), obj(event))

        event.var1[:] = [45.2, ] # <- out of range
        event.var2[:] = [22.8, ]
        event.var3[:] = [234.9, ]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [15.2, ] # <- out of range
        event.var2[:] = [82.8, ] # <- out of range
        event.var3[:] = [34.9, ]
        self.assertEqual(( ), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_simple(unittest.TestCase):

    def test_1Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            keyIndices = (2, )
        )
        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, 20.2, 10.2, 10.8]
        self.assertEqual(
            (
                ((10, ), ( )),
            ), obj(event))

        event.var1[:] = [12.5, 20.2, 35.2, 10.8] # out of range of the binning
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.5, 20.2] # out of range of the list
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.5, 32.2, 10.2, 10.8] # another element out of range
        self.assertEqual(
            (
                ((10, ), ( )),
            ), obj(event))

    def test_NoneKey_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            valAttrNames = ('var1', ),
            valIndices = (2, )
        )
        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, 20.2, 10.2, 10.8]
        self.assertEqual(
            (
                (( ), (10.2, )),
            ), obj(event))

    def test_1Key_keyIndices_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            keyIndices = (2, ),
            valAttrNames = ('var2', ),
            valIndices = (2, )
        )
        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, 20.2, 10.2, 10.8]
        event.var2[:] = [30.1, 42.5, 19.2, 71.2]
        self.assertEqual(
            (
                ((10, ), (19.2, )),
            ), obj(event))

        event.var1[:] = [12.5, 20.2, 30.2, 10.8] # out of range of the binning
        event.var2[:] = [30.1, 42.5, 19.2, 71.2]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.5, 20.2]
        event.var2[:] = [30.1, 42.5, 19.2, 71.2]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.5, 20.2, 30.2, 10.8]
        event.var2[:] = [30.1, 42.5] # out of range of the list
        self.assertEqual(( ), obj(event))

    def test_3Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3'),
            binnings = (MockBinningFloor(), MockBinningFloor(max = 300), MockBinningFloor()),
            keyIndices = (1, None, 2))

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, 8.2, 6.1]
        event.var2[:] = [232.2, ]
        event.var3[:] = [111.1, 222.2, 333.3]
        self.assertEqual(
            (
                ((8, 232, 333), ( )),
            ), obj(event))

        event.var1[:] = [12.5, 8.2, 6.1]
        event.var2[:] = [ ] # out of range of the list
        event.var3[:] = [111.1, 222.2, 333.3]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.5, 8.2, 6.1]
        event.var2[:] = [421.5] # out of range of binning
        event.var3[:] = [111.1, 222.2, 333.3]
        self.assertEqual(( ), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_wildcard(unittest.TestCase):

    def test_1Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningFloor(max = 30), ),
            keyIndices = ('*', )
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12.8, 8.6, 6.2]
        self.assertEqual(
            (
                ((12, ), ( )),
                (( 8, ), ( )),
                (( 6, ), ( )),
            ), obj(event))

        event.var1[:] = [12.8, 38.6, 6.2] # 1 element out of range
        self.assertEqual(
            (
                ((12, ), ( )),
                (( 6, ), ( )),
            ), obj(event))

        event.var1[:] = [42.8, 38.6, 56.2] # all elements out of range
        self.assertEqual(( ), obj(event))

        event.var1[:] = [ ] # list empty
        self.assertEqual(( ), obj(event))

    def test_2Keys_keyIndices_NoneVal_1Wildcard(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50)),
            keyIndices = ('*', None)
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12.8, 8.6, 6.2]
        event.var2[:] = [35.2, ]
        self.assertEqual(
            (
                ((12, 35), ( )),
                (( 8, 35), ( )),
                (( 6, 35), ( )),
            ), obj(event))

        event.var1[:] = [12.8, 38.6, 6.2] # 1 element out of range
        event.var2[:] = [35.2, ]
        self.assertEqual(
            (
                ((12, 35), ( )),
                (( 6, 35), ( )),
            ), obj(event))

        event.var1[:] = [ ] # list empty
        event.var2[:] = [35.2, ]
        self.assertEqual(( ), obj(event))

        event.var1[:] = [12.8, 8.6, 6.2]
        event.var2[:] = [ ] # list empty
        self.assertEqual(( ), obj(event))

        event.var1[:] = [ ] # list empty
        event.var2[:] = [ ] # list empty
        self.assertEqual(( ), obj(event))

    def test_2Keys_keyIndices_NoneVal_2Wildcards(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50)),
            keyIndices = ('*', '*')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12.8, 18.6, 26.2]
        event.var2[:] = [15.2, 22.3, 12.8]
        self.assertEqual(
            (
                ((12, 15), ( )),
                ((12, 22), ( )),
                ((12, 12), ( )),
                ((18, 15), ( )),
                ((18, 22), ( )),
                ((18, 12), ( )),
                ((26, 15), ( )),
                ((26, 22), ( )),
                ((26, 12), ( )),
            ),
            obj(event)
        )

        event.var1[:] = [12.8, 38.6, 26.2]  # 1 element out of range
        event.var2[:] = [55.2, 22.3, 12.8]  # 1 element out of range
        self.assertEqual(
            (
                ((12, 22), ( )),
                ((12, 12), ( )),
                ((26, 22), ( )),
                ((26, 12), ( )),
            ),
            obj(event)
        )

        event.var1[:] = [ ]  # empty list
        event.var2[:] = [55.2, 22.3, 12.8] # 1 element out of range
        self.assertEqual(( ), obj(event))

    def test_2Keys_keyIndices_2Val_valIndices_4Wildcards(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningFloor(max = 30), MockBinningFloor(max = 50)),
            keyIndices = ('*', '*'),
            valAttrNames = ('var3', 'var4'),
            valIndices = ('*', '*'),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5, 6.2]
        event.var2[:] = [ 5.1, 60.2, 2.8] # 1 element out of range
        event.var3[:] = [20.2, 21.9, 22.4]
        event.var4[:] = [44.4, 55.5]
        self.assertEqual(
            (
                ((12, 5), (20.2, 44.4)),
                ((12, 5), (20.2, 55.5)),
                ((12, 5), (21.9, 44.4)),
                ((12, 5), (21.9, 55.5)),
                ((12, 5), (22.4, 44.4)),
                ((12, 5), (22.4, 55.5)),
                ((12, 2), (20.2, 44.4)),
                ((12, 2), (20.2, 55.5)),
                ((12, 2), (21.9, 44.4)),
                ((12, 2), (21.9, 55.5)),
                ((12, 2), (22.4, 44.4)),
                ((12, 2), (22.4, 55.5)),
                (( 6, 5), (20.2, 44.4)),
                (( 6, 5), (20.2, 55.5)),
                (( 6, 5), (21.9, 44.4)),
                (( 6, 5), (21.9, 55.5)),
                (( 6, 5), (22.4, 44.4)),
                (( 6, 5), (22.4, 55.5)),
                (( 6, 2), (20.2, 44.4)),
                (( 6, 2), (20.2, 55.5)),
                (( 6, 2), (21.9, 44.4)),
                (( 6, 2), (21.9, 55.5)),
                (( 6, 2), (22.4, 44.4)),
                (( 6, 2), (22.4, 55.5)),
            ), obj(event))

        event.var1[:] = [12.5, 6.2]
        event.var2[:] = [ 5.1, 60.2, 2.8] # 1 element out of range
        event.var3[:] = [20.2, 21.9, 22.4]
        event.var4[:] = [] # empty list
        self.assertEqual(( ), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_backref(unittest.TestCase):

    def test_3Keys_keyIndices_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3'),
            binnings = (MockBinningFloor(), MockBinningFloor(max = 40), MockBinningFloor(max = 80)),
            keyIndices = (None, '(*)', '\\1'),
            valAttrNames = ('var4', ),
            valIndices = ('\\1', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [12.5]
        event.var2[:] = [  5.2,  40.2,   2.4,   4.2, 30.9] # 1 element out of range
        event.var3[:] = [ 10.8,  13.6,  20.2,  85.7, 22.3, 50.1] # 1 element out of range
        event.var4[:] = [  100,   200,   300,  400]
        self.assertEqual(
            (
                ((12, 5, 10), (100, )),
                ((12, 2, 20), (300, ))
            ),
            obj(event)
        )

        event.var1[:] = [12.5]
        event.var2[:] = [  5.2,  40.2,  2.4,  4.2, 45.2] # 1 element out of range
        event.var3[:] = [ 85.9,  13.6, 90.1, 81.2, 22.3, 50.1] # 3 elements out of range
        event.var4[:] = [  100,   200,  300,  400]
        self.assertEqual(( ), obj(event))

    def test_4Keys_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3', 'var4'),
            binnings = (MockBinningFloor(), MockBinningFloor(max = 40), MockBinningFloor(max = 80), MockBinningFloor()),
            keyIndices = (None, '(*)', '\\1', '*')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [ 12.5]
        event.var2[:] = [  5.2,  40.2,   2.4,   4.2, 30.9] # 1 element out of range
        event.var3[:] = [ 10.8,  13.6,  20.2,  85.7, 22.3, 50.1] # 1 element out of range
        event.var4[:] = [  100,   200]
        self.assertEqual(
            (
                ((12,  5, 10, 100), ( )),
                ((12,  5, 10, 200), ( )),
                ((12,  2, 20, 100), ( )),
                ((12,  2, 20, 200), ( )),
                ((12, 30, 22, 100), ( )),
                ((12, 30, 22, 200), ( )),
            ),
            obj(event)
        )

        event.var1[:] = [ 12.5]
        event.var2[:] = [  5.2,  40.2,  52.4,   4.2, 60.9] # 1 element out of range
        event.var3[:] = [ 90.8,  13.6,  20.2,  85.7, 22.3, 50.1] # 1 element out of range
        event.var4[:] = [  100,   200]
        self.assertEqual(( ), obj(event))

    def test_NoneKeys_4Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            valAttrNames = ('var1', 'var2', 'var3', 'var4'),
            valIndices = (None, '(*)', '\\1', '*')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [ 12.5]
        event.var2[:] = [  5.2,   4.2, 30.9]
        event.var3[:] = [ 10.8,  13.6,  20.2, 22.3, 50.1]
        event.var4[:] = [  100,   200]
        self.assertEqual(
            (
                (( ), (12.5,  5.2, 10.8, 100)),
                (( ), (12.5,  5.2, 10.8, 200)),
                (( ), (12.5,  4.2, 13.6, 100)),
                (( ), (12.5,  4.2, 13.6, 200)),
                (( ), (12.5, 30.9, 20.2, 100)),
                (( ), (12.5, 30.9, 20.2, 200)),
            ),
            obj(event)
        )

    def test_4Keys_keyIndices_1Val_valIndices_2Backrefs(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('ev', 'jet_pt', 'jet_eta', 'mu_pt'),
            binnings = (MockBinningFloor(), MockBinningFloor(max = 40), MockBinningFloor(max = 4), MockBinningFloor(max = 40)),
            keyIndices = (None, '(*)', '\\1', '(*)'),
            valAttrNames = ('mu_eta', ),
            valIndices = ('\\2', )
        )

        event = MockEvent()
        event.ev = [ ]
        event.jet_pt = [ ]
        event.jet_eta = [ ]
        event.mu_pt = [ ]
        event.mu_eta = [ ]
        obj.begin(event)

        event.ev[:] = [1001]
        event.jet_pt[:]  = [15.0, 12.0, 45.2, 10.0] # 1 element out of range
        event.jet_eta[:] = [ 4.5,  1.2,  2.2,  0.5] # 1 element out of range
        event.mu_pt[:]   = [20.0, 41.0, 13.0] # 1 element out of range
        event.mu_eta[:]  = [ 2.5,  0.2, 1.0]

        self.assertEqual(
            (
                ((1001, 12, 1, 20, ), (2.5, )),
                ((1001, 12, 1, 13, ), (1.0, )),
                ((1001, 10, 0, 20, ), (2.5, )),
                ((1001, 10, 0, 13, ), (1.0, )),
            ),
            obj(event)
        )

        event.ev[:] = [1001]
        event.jet_pt[:]  = [15.0, None, None, 10.0]
        event.jet_eta[:] = [None,  1.2,  2.2,  None]
        event.mu_pt[:]   = [20.0, 11.0, 13.0]
        event.mu_eta[:]  = [2.5,  None, 1.0]

        self.assertEqual(( ), obj(event))

    def test_back_reference_example_twice(self):
        obj = Counter.KeyValueComposer(
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
