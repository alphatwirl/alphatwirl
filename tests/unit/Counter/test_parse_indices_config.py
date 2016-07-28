import AlphaTwirl.Counter as Counter
import unittest

##__________________________________________________________________||
class Test_parse_indices_config(unittest.TestCase):

    def test_1(self):
        Counter.parse_indices_config((None, None, '(*)', '(*)', '\\1', '\\2'))

##__________________________________________________________________||
