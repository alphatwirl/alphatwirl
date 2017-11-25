import unittest

import io
import textwrap

##__________________________________________________________________||
hasPandas = False
try:
    import pandas as pd
    hasPandas = True
except ImportError:
    pass

##__________________________________________________________________||
tbl_01_txt = r"""
   v1        v2
   10       AAA
   20     "BBB"
   30     'BBB'
   30   \"BBB\"
   40   "\"BBB"
   50   "\"B BB"
   60    " xyz"
"""
tbl_01_txt = tbl_01_txt[tbl_01_txt.find('\n') + 1:] # remove 1st line
tbl_01_txt = textwrap.dedent(tbl_01_txt)
tbl_01_txt = tbl_01_txt.encode()

##__________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class TestPandasQuotes(unittest.TestCase):

    def test_one(self):
        input = io.BytesIO(tbl_01_txt)
        tbl = pd.read_table(input, delim_whitespace = True, escapechar = '\\')

        expected = [
            'AAA',    # no quote
            'BBB',    # double quote (striped)
            "'BBB'",  # single quote (still there)
            '"BBB"',  # double quote (escaped)
            '"BBB',   # double quote (escaped) within double quote
            '"B BB',  # double quote (escaped with space)
            ' xyz'    # start with space
        ]

        actual = tbl.v2.values.tolist()
        self.assertEqual(expected, actual)

##__________________________________________________________________||
