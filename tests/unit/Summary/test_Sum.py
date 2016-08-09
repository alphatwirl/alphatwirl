import unittest
import numpy as np

from AlphaTwirl.Summary import Sum

##__________________________________________________________________||
class TestSum(unittest.TestCase):

    def assert_np_dict_frame(self, f1, f2):
        self.assertEqual(sorted(f1.keys()), sorted(f2.keys()))
        for k in sorted(f1.keys()):
            np.testing.assert_equal(f1[k], f2[k])

    def test_add_1d_val(self):
        obj = Sum()

        obj.add(1, 10)
        expected  = {1: np.array((10, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1, 12)
        expected  = {1: np.array((22, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1, 2, weight = 2)
        expected  = {1: np.array((26, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(2, 3, weight = 3.2)
        expected  = {
            1: np.array((   26, )),
            2: np.array((3*3.2, )),
        }
        self.assert_np_dict_frame(expected, obj.results())
        self.assertEqual(expected, obj.results()) # this works

    def test_add_int_to_float_val(self):
        obj = Sum()

        obj.add(1, 10) # int
        expected  = {1: np.array((10, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1, 12.4) # float
        expected  = {1: np.array((22.4, ))}
        self.assert_np_dict_frame(expected, obj.results())

    def test_add_int_to_float_weight(self):
        obj = Sum()

        obj.add(1, 10) # int
        expected  = {1: np.array((10, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add(1, 12, weight = 1.2) # int val, float weight
        expected  = {1: np.array((24.4, ))}
        self.assert_np_dict_frame(expected, obj.results())

    def test_add_key(self):
        obj = Sum()
        obj.add_key(1)
        expected  = {1: np.array((0, ))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add_key(3)
        obj.add_key(5)
        expected  = {
            1: np.array((0, )),
            3: np.array((0, )),
            5: np.array((0, ))
        }
        self.assert_np_dict_frame(expected, obj.results())

    def test_add_key_initial_val(self):
        obj = Sum(initial_val = (2, 3))
        obj.add_key(1)
        expected  = {1: np.array((2, 3))}
        self.assert_np_dict_frame(expected, obj.results())

        obj.add_key(3)
        obj.add_key(5)
        expected  = {
            1: np.array((2, 3)),
            3: np.array((2, 3)),
            5: np.array((2, 3))
        }
        self.assert_np_dict_frame(expected, obj.results())

##__________________________________________________________________||
