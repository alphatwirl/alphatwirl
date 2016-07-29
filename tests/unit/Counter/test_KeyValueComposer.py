import AlphaTwirl.Counter as Counter
import unittest
import logging

##__________________________________________________________________||
class MockEvent(object):
    pass

##__________________________________________________________________||
class MockBinningEcho(object):
    def __call__(self, val):
        return val

    def next(self, val):
        return val + 1

##__________________________________________________________________||
class MockBinningNone(object):
    def __call__(self, val):
        return None

    def next(self, val):
        return val + 1

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
            binnings = (MockBinningEcho(), ),
            valAttrNames = ('var2', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        event.var2[:] = [20, ]
        self.assertEqual((((12, ), ), ((20, ), )), obj(event))

    def test_1Key_1Val_mix_list_tuple(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ['var1', ], # <- list
            binnings = (MockBinningEcho(), ),
            valAttrNames = ('var2', ), # <- tuple
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        event.var2[:] = [20, ]
        self.assertEqual((((12, ), ), ((20, ), )), obj(event))

    def test_1Key_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            valAttrNames = None, # <- None
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((((12, ), ), None), obj(event))

    def test_1Key_emptyVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            valAttrNames = (), # <- empty
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((((12, ), ), None), obj(event))

    def test_NoneKey_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = None, # <- None
            valAttrNames = ('var1', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((None, ((12, ), )), obj(event))

    def test_emptyKey_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = (), # <- empty
            valAttrNames = ('var1', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((None, ((12, ), )), obj(event))

    def test_NoneKey_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = None,
            valAttrNames = None,
        )

        event = MockEvent()
        obj.begin(event)

        self.assertEqual((None, None), obj(event))

    def test_2Keys_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho())
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [15, ]
        event.var2[:] = [22, ]
        self.assertEqual((((15, 22), ), None), obj(event))

    def test_2Keys_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho()),
            valAttrNames = ('var3', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        obj.begin(event)

        event.var1[:] = [15, ]
        event.var2[:] = [22, ]
        event.var3[:] = [101, ]
        self.assertEqual((((15, 22), ), ((101, ), )), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_bin_out_of_range(unittest.TestCase):

    def test_1Key_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningNone(), )
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((( ), None), obj(event))

    def test_2Keys_NoneVal_1(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningNone(), MockBinningEcho())
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [15, ]
        event.var2[:] = [22, ]
        self.assertEqual((( ), None), obj(event))

    def test_2Keys_NoneVal_2(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningNone())
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [15, ]
        event.var2[:] = [22, ]
        self.assertEqual((( ), None), obj(event))

    def test_1Key_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningNone(), ),
            valAttrNames = ('var2', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        event.var2[:] = [20, ]
        self.assertEqual((( ), ( )), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_simple(unittest.TestCase):

    def test_1Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices = (0, )
        )
        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((((12, ), ), None), obj(event))

    def test_NoneKey_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            valAttrNames = ('var1', ),
            valIndices = (0, )
        )
        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        self.assertEqual((None, ((12, ), )), obj(event))

    def test_1Key_keyIndices_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices = (0, ),
            valAttrNames = ('var2', ),
            valIndices = (0, )
        )
        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, ]
        event.var2[:] = [20, ]
        self.assertEqual((((12, ), ), ((20, ), )), obj(event))

    def test_3Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3'),
            binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho()),
            keyIndices = (1, None, 2))

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [232, ]
        event.var3[:] = [111, 222, 333]
        self.assertEqual((((8, 232, 333), ), None), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_simple_out_of_range(unittest.TestCase):

    def test_1Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices =  (1, )
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        self.assertEqual((((8, ), ), None), obj(event))

        event.var1[:] = [3, ]
        self.assertEqual((( ), None), obj(event))

    def test_1Key_keyIndices_1Val(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices =  (1, ),
            valAttrNames = ('var2', ),
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [33]
        self.assertEqual((((8, ), ), ((33, ), )), obj(event))

        event.var1[:] = [3, ]
        event.var2[:] = [44]
        self.assertEqual((( ), ( )), obj(event))

    def test_1Key_keyIndices_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices = (1, ),
            valAttrNames = ('var2', ),
            valIndices = (1, )
        )
        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 13]
        event.var2[:] = [20, 30]
        self.assertEqual((((13, ), ), ((30, ), )), obj(event))

        event.var1[:] = [22]
        event.var2[:] = [25, 35]
        self.assertEqual((( ), ( )), obj(event))

        event.var1[:] = [32, 44]
        event.var2[:] = [52]
        self.assertEqual((( ), ( )), obj(event))

    def test_NoneKey_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            valAttrNames = ('var1', ),
            valIndices = (1, )
        )
        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 13]
        self.assertEqual((None, ((13, ), )), obj(event))

        event.var1[:] = [22]
        self.assertEqual((None, ( )), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_wildcard(unittest.TestCase):

    def test_1Key_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', ),
            binnings = (MockBinningEcho(), ),
            keyIndices = ('*', )
        )

        event = MockEvent()
        event.var1 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        self.assertEqual((((12, ), (8, ), (6, )), None), obj(event))

    def test_2Keys_keyIndices_NoneVal_1Wildcard(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho()),
            keyIndices = ('*', None)
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [5, ]
        self.assertEqual((((12, 5), (8, 5), (6, 5)), None), obj(event))

    def test_2Keys_keyIndices_NoneVal_2Wildcards(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho()),
            keyIndices = ('*', '*')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [5, None, 2]
        self.assertEqual((((12, 5), (12, 2), (8, 5), (8, 2), (6, 5), (6, 2)), None), obj(event))

    def test_2Keys_keyIndices_2Val_valIndices_4Wildcards(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningEcho()),
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

        event.var1[:] = [12, 6]
        event.var2[:] = [5, None, 2]
        event.var3[:] = [20, 21, 22]
        event.var4[:] = [44, 55]
        self.assertEqual(
            (
                (
                    (12, 5), (12, 5), (12, 5), (12, 5), (12, 5), (12, 5),
                    (12, 2), (12, 2), (12, 2), (12, 2), (12, 2), (12, 2),
                    (6, 5), (6, 5), (6, 5), (6, 5), (6, 5), (6, 5),
                    (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2)
                ),
                (
                    (20, 44), (20, 55), (21, 44), (21, 55), (22, 44), (22, 55),
                    (20, 44), (20, 55), (21, 44), (21, 55), (22, 44), (22, 55),
                    (20, 44), (20, 55), (21, 44), (21, 55), (22, 44), (22, 55),
                    (20, 44), (20, 55), (21, 44), (21, 55), (22, 44), (22, 55)
                )
            ), obj(event))

##__________________________________________________________________||
class TestKeyValueComposer_indices_wildcard_bin_out_of_range(unittest.TestCase):

    def test_2Keys_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningNone()),
            keyIndices =  ('*', None)
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [5, ]
        self.assertEqual((( ), None), obj(event))

    def test_2Keys_keyIndices_2Vals(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2'),
            binnings = (MockBinningEcho(), MockBinningNone()),
            keyIndices =  ('*', None),
            valAttrNames = ('var3', 'var4')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [12, 8, 6]
        event.var2[:] = [5, ]
        event.var3[:] = [15, ]
        event.var4[:] = [25, ]
        self.assertEqual((( ), ( )), obj(event))


##__________________________________________________________________||
class TestKeyValueComposer_indices_backref(unittest.TestCase):

    def test_3Keys_keyIndices_1Val_valIndices(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3'),
            binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho()),
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

        event.var1[:] = [12]
        event.var2[:] = [  5,  None,   2,    4, 30]
        event.var3[:] = [ 10,    13,  20, None, 22, 50]
        event.var4[:] = [100,   200, 300,  400]
        self.assertEqual(
            (
                (
                    (12, 5, 10), (12, 2, 20),
                ),
                ((100, ), (300, ))
            ),
            obj(event)
        )

        event.var1[:] = [12]
        event.var2[:] = [   5,  None,     2,    4, None]
        event.var3[:] = [None,    13,  None, None, 22, 50]
        event.var4[:] = [100,   200, 300,  400]
        self.assertEqual((( ), ( )), obj(event))

    def test_4Keys_keyIndices_NoneVal(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('var1', 'var2', 'var3', 'var4'),
            binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho(), MockBinningEcho()),
            keyIndices = (None, '(*)', '\\1', '*')
        )

        event = MockEvent()
        event.var1 = [ ]
        event.var2 = [ ]
        event.var3 = [ ]
        event.var4 = [ ]
        obj.begin(event)

        event.var1[:] = [12]
        event.var2[:] = [5,  None,   2,    4, 30]
        event.var3[:] = [10,   13,  20, None, 22, 50]
        event.var4[:] = [100, 200]
        self.assertEqual(
            (
                (
                    (12, 5, 10, 100), (12, 5, 10, 200),
                    (12, 2, 20, 100), (12, 2, 20, 200),
                    (12, 30, 22, 100), (12, 30, 22, 200)
                ),
                None
            ),
            obj(event)
        )

        event.var1[:] = [12]
        event.var2[:] = [   5,  None, None,    4, None]
        event.var3[:] = [None,    13,   20, None, 22, 50]
        event.var4[:] = [100, 200]
        self.assertEqual((( ), None), obj(event))

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

        event.var1[:] = [12]
        event.var2[:] = [5,  None,   2,    4, 30]
        event.var3[:] = [10,   13,  20, None, 22, 50]
        event.var4[:] = [100, 200]
        self.assertEqual(
            (
                None,
                (
                    (12, 5, 10, 100), (12, 5, 10, 200),
                    (12, 2, 20, 100), (12, 2, 20, 200),
                    (12, 30, 22, 100), (12, 30, 22, 200)
                )
            ),
            obj(event)
        )

        event.var1[:] = [12]
        event.var2[:] = [None,  None,   2,    4, 30]
        event.var3[:] = [  10,    13, None, None, None, 50]
        event.var4[:] = [100, 200]
        self.assertEqual((None, ( )), obj(event))

    def test_4Keys_keyIndices_1Val_valIndices_2Backrefs(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('ev', 'jet_pt', 'jet_eta', 'mu_pt'),
            binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho(), MockBinningEcho()),
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
        event.jet_pt[:]  = [15.0, 12.0, None, 10.0]
        event.jet_eta[:] = [None,  1.2,  2.2,  0.5]
        event.mu_pt[:]   = [20.0, 11.0, 13.0]
        event.mu_eta[:]  = [2.5,  None, 1.0]

        self.assertEqual(
            (
                (
                    (1001, 12.0, 1.2, 20.0, ),
                    (1001, 12.0, 1.2, 13.0, ),
                    (1001, 10.0, 0.5, 20.0, ),
                    (1001, 10.0, 0.5, 13.0, ),
                ),
                (
                    (2.5, ),
                    (1.0, ),
                    (2.5, ),
                    (1.0, ),
                ),
            ),
            obj(event)
        )

        event.ev[:] = [1001]
        event.jet_pt[:]  = [15.0, None, None, 10.0]
        event.jet_eta[:] = [None,  1.2,  2.2,  None]
        event.mu_pt[:]   = [20.0, 11.0, 13.0]
        event.mu_eta[:]  = [2.5,  None, 1.0]

        self.assertEqual(((), ()), obj(event)
        )

    def test_back_reference_example_twice(self):
        obj = Counter.KeyValueComposer(
            keyAttrNames = ('ev', 'jet_pt', 'jet_eta', 'mu_pt', 'mu_eta', 'jet_phi'),
            binnings = (MockBinningEcho(), MockBinningEcho(), MockBinningEcho(), MockBinningEcho(), MockBinningEcho(), MockBinningEcho()),
            keyIndices = (None, '(*)', '\\1', '(*)', '\\2', '\\1'),
            valAttrNames = ('jet_energy', 'muon_energy'),
            valIndices = ('\\1', '\\2'),
        )

        event = MockEvent()
        event.ev = [ ]
        event.jet_pt = [ ]
        event.jet_eta = [ ]
        event.mu_pt = [ ]
        event.mu_eta = [ ]
        event.jet_phi = [ ]
        event.jet_energy = [ ]
        event.muon_energy = [ ]
        obj.begin(event)

        event.ev[:] = [1001]
        event.jet_pt[:]  = [15.0, 12.0, None, 10.0]
        event.jet_eta[:] = [None,  1.2,  2.2,  0.5]
        event.mu_pt[:]   = [20.0, 11.0, 13.0]
        event.mu_eta[:]  = [2.5,  None, 1.0]
        event.jet_phi[:] = [ 0.1,  0.6,  None, 0.3]
        event.jet_energy[:] = [21.0, 13.0, 15.0, 11.0]
        event.muon_energy[:] = [22.0, 15.0, 16.0]

        self.assertEqual(
            (
                (
                    (1001, 12.0, 1.2, 20.0, 2.5, 0.6),
                    (1001, 12.0, 1.2, 13.0, 1.0, 0.6),
                    (1001, 10.0, 0.5, 20.0, 2.5, 0.3),
                    (1001, 10.0, 0.5, 13.0, 1.0, 0.3),
                ),
                (
                    (13.0, 22.0),
                    (13.0, 16.0),
                    (11.0, 22.0),
                    (11.0, 16.0)
                )
            ),
            obj(event)
        )

##__________________________________________________________________||
