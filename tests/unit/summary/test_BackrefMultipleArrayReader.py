import unittest
import alphatwirl.summary as summary

##__________________________________________________________________||
class TestBackrefMultipleArrayReader_init(unittest.TestCase):

    def test_argument_length(self):
        self.assertRaises(
            ValueError,
            summary.BackrefMultipleArrayReader,
            arrays = [[ ] ],
            idxs_conf = ( ),
            )

        self.assertRaises(
            ValueError,
            summary.BackrefMultipleArrayReader,
            arrays = [[ ], [ ]],
            idxs_conf = (2, 3, 4),
            )

        self.assertRaises(
            ValueError,
            summary.BackrefMultipleArrayReader,
            arrays = [[ ], [ ]],
            idxs_conf = (2, 3),
            backref_idxs = (None, None, 1)
            )

    def test_argument_length_2(self):
            summary.BackrefMultipleArrayReader(
                arrays = [[ ], [ ]],
                idxs_conf = (1, 2),
                backref_idxs = None
            )

##__________________________________________________________________||
class TestBackrefMultipleArrayReader_simple(unittest.TestCase):

    def test_empty(self):
        arrays = [ ]
        idxs_conf = ( )
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        self.assertEqual((( ), ), obj.read())

    def test_1_element(self):
        arrays = [[ ]]
        idxs_conf = (0, )
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [12, 13, 14]
        self.assertEqual(((12, ), ), obj.read())

        arrays[0][:] = [ ]
        self.assertEqual(( ), obj.read())

    def test_3_elements(self):
        arrays = [[], [], []]
        idxs_conf = (1, 0, 2)
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [105]
        arrays[2][:] = [33, 35, 37]
        self.assertEqual(((13, 105, 37 ), ), obj.read())

        arrays[0][:] = [12] # <- out of range
        arrays[1][:] = [105]
        arrays[2][:] = [33, 35, 37]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [ ] # <- out of range
        arrays[2][:] = [33, 35, 37]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [105]
        arrays[2][:] = [33, 35] # <- out of range
        self.assertEqual(( ), obj.read())


##__________________________________________________________________||
class TestBackrefMultipleArrayReader_wildcard(unittest.TestCase):

    def test_1_wildcard(self):
        arrays = [[ ]]
        idxs_conf = ('*', )
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12]
        self.assertEqual(((12,), ), obj.read())

        arrays[0][:] = [12, 13]
        self.assertEqual(((12,), (13,)), obj.read())

        arrays[0][:] = [12, 13, 14]
        self.assertEqual(((12,), (13,), (14,)), obj.read())

    def test_1_index_1_wildcard(self):
        arrays = [[ ], [ ]]
        idxs_conf = (1, '*')
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [ ]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [203, 204, 205]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [203, 204, 205]
        arrays[1][:] = [12]
        self.assertEqual(((204, 12), ), obj.read())

        arrays[0][:] = [203, 204, 205]
        arrays[1][:] = [12, 13, 14]
        self.assertEqual(((204, 12), (204, 13), (204, 14)), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [12, 13, 14]
        self.assertEqual(( ), obj.read())

    def test_2_wildcards(self):
        arrays = [[ ], [ ]]
        idxs_conf = ('*', '*')
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [ ]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104, 105]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12]
        arrays[1][:] = [104]
        self.assertEqual(((12, 104), ), obj.read())

        arrays[0][:] = [12, 13]
        arrays[1][:] = [104]
        self.assertEqual(((12, 104), (13, 104)), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104]
        self.assertEqual(((12, 104), (13, 104), (14, 104)), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104, 105]
        self.assertEqual(
            (
                (12, 104), (12, 105),
                (13, 104), (13, 105),
                (14, 104), (14, 105)
            ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104, 105, 106]
        self.assertEqual(
            (
                (12, 104), (12, 105), (12, 106),
                (13, 104), (13, 105), (13, 106),
                (14, 104), (14, 105), (14, 106)
            ), obj.read())

    def test_3_wildcards(self):
        arrays = [[ ], [ ], [ ]]
        idxs_conf = ('*', '*', '*')
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [ ]
        arrays[1][:] = [ ]
        arrays[2][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13]
        arrays[1][:] = [ ]
        arrays[2][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104]
        arrays[2][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104]
        arrays[2][:] = [1001, 1002, 1003]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104, 105]
        arrays[2][:] = [1001, 1002, 1003]
        self.assertEqual(
            (
                (12, 104, 1001), (12, 104, 1002), (12, 104, 1003),
                (12, 105, 1001), (12, 105, 1002), (12, 105, 1003),
                (13, 104, 1001), (13, 104, 1002), (13, 104, 1003),
                (13, 105, 1001), (13, 105, 1002), (13, 105, 1003),
                (14, 104, 1001), (14, 104, 1002), (14, 104, 1003),
                (14, 105, 1001), (14, 105, 1002), (14, 105, 1003),
            ), obj.read())

    def test_2_indices_wildcards(self):
        arrays = [[ ], [ ], [ ], [ ], [ ]]
        idxs_conf = (1, '*', '*', 2, '*')
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf
        )

        arrays[0][:] = [ ]
        arrays[1][:] = [ ]
        arrays[2][:] = [ ]
        arrays[3][:] = [ ]
        arrays[4][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [55, 66, 77]
        arrays[1][:] = [12, 13, 14]
        arrays[2][:] = [104, 105]
        arrays[3][:] = [222, 333, 444, 555]
        arrays[4][:] = [1001, 1002, 1003]
        self.assertEqual(
            (
                (66, 12, 104, 444, 1001), (66, 12, 104, 444, 1002), (66, 12, 104, 444, 1003),
                (66, 12, 105, 444, 1001), (66, 12, 105, 444, 1002), (66, 12, 105, 444, 1003),
                (66, 13, 104, 444, 1001), (66, 13, 104, 444, 1002), (66, 13, 104, 444, 1003),
                (66, 13, 105, 444, 1001), (66, 13, 105, 444, 1002), (66, 13, 105, 444, 1003),
                (66, 14, 104, 444, 1001), (66, 14, 104, 444, 1002), (66, 14, 104, 444, 1003),
                (66, 14, 105, 444, 1001), (66, 14, 105, 444, 1002), (66, 14, 105, 444, 1003),
            ), obj.read())

        # #
        # # measure time
        # # python -m unittest tests.unit.summary.test_BackrefMultipleArrayReader.TestBackrefMultipleArrayReader_wildcard.test_2_indices_wildcards
        # from datetime import datetime
        # tick = datetime.now()
        # for i in range(100000): obj.read()
        # tock = datetime.now()
        # diff = tock - tick
        # print 'time: ', diff.total_seconds()
        # 
        # # time:  0.930973 08/05 12:14
        # # time:  0.507036 08/05 13:14

##__________________________________________________________________||
class TestBackrefMultipleArrayReader_backref(unittest.TestCase):

    def test_1_wildcard_1_backref(self):
        arrays = [[ ], [ ]]
        idxs_conf = ('*', None)
        backref_idxs = [None, 0]
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf, backref_idxs = backref_idxs
        )

        arrays[0][:] = [ ]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12]
        arrays[1][:] = [104]
        self.assertEqual(((12, 104), ), obj.read())

        arrays[0][:] = [12]
        arrays[1][:] = [ ]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13]
        arrays[1][:] = [104, 105]
        self.assertEqual(((12, 104), (13, 105)), obj.read())

        arrays[0][:] = [12, 13]
        arrays[1][:] = [104]
        self.assertEqual(((12, 104), ), obj.read())

        arrays[0][:] = [12]
        arrays[1][:] = [104, 105]
        self.assertEqual(((12, 104), ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104, 105, 106]
        self.assertEqual(((12, 104), (13, 105), (14, 106)), obj.read())

        arrays[0][:] = [ ]
        arrays[1][:] = [104, 105, 106]
        self.assertEqual(( ), obj.read())

        arrays[0][:] = [12, 13, 14]
        arrays[1][:] = [104, 105]
        self.assertEqual(((12, 104), (13, 105)), obj.read())

    def test_1_index_2_wildcards_4_backrefs(self):
        arrays = [[ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ]]
        idxs_conf = (0, '*', None, '*', None, None, None, None)
        backref_idxs = [None, None, 1, None, 3, 1, 1, 3]
        obj = summary.BackrefMultipleArrayReader(
            arrays = arrays, idxs_conf = idxs_conf, backref_idxs = backref_idxs
        )

        arrays[0][:] = [1001]

        arrays[1][:] = [ 12,  13,  14,  15]
        arrays[2][:] = [104, 105, 106, 107]
        arrays[5][:] = [403, 404, 405] # <- shorter
        arrays[6][:] = [207, 208, 209, 210]

        arrays[3][:] = [51, 52] # <- shorter
        arrays[4][:] = [84, 85, 86]
        arrays[7][:] = [91, 92, 93]
        self.assertEqual(
            (
                (1001, 12, 104, 51, 84, 403, 207, 91),
                (1001, 12, 104, 52, 85, 403, 207, 92),
                (1001, 13, 105, 51, 84, 404, 208, 91),
                (1001, 13, 105, 52, 85, 404, 208, 92),
                (1001, 14, 106, 51, 84, 405, 209, 91),
                (1001, 14, 106, 52, 85, 405, 209, 92)
            ), obj.read())

        # #
        # # measure time
        # # python -m unittest tests.unit.summary.test_BackrefMultipleArrayReader.TestBackrefMultipleArrayReader_backref.test_1_index_2_wildcards_4_backrefs
        # 
        # # import cProfile, pstats, StringIO
        # from datetime import datetime
        # 
        # # pr = cProfile.Profile()
        # # pr.enable()
        # 
        # tick = datetime.now()
        # for i in range(30000): obj.read()
        # tock = datetime.now()
        # 
        # # pr.disable()
        # 
        # diff = tock - tick
        # print 'time: ', diff.total_seconds()
        # 
        # # s = StringIO.StringIO()
        # # sortby = 'cumulative'
        # # ps = pstats.Stats(pr, stream = s).strip_dirs().sort_stats(sortby)
        # # ps.print_stats()
        # # print s.getvalue()
        # 
        # # time:  1.188824 08/05 10:31 # before starting refactoring
        # # time:  0.975665 08/05 12:08
        # # time:  0.611698 08/05 12:20 # if comment out self._unzip_and_read_arrays(zipped)
        # # time:  0.527065 08/05 12:24 # use _zipped2, _zipped3

##__________________________________________________________________||
