from AlphaTwirl.HeppyResult import ReadComponentConfig
import unittest
import cStringIO

##____________________________________________________________________________||
sample_cmp_cfg = """MCComponent: QCD_HT_100To250_Chunk0
	addWeight      :   1.0
	efficiency     :   CFG: eff
	triggers       :   []
	xSection       :   28730000
"""

##____________________________________________________________________________||
class TestReadComponentConfig(unittest.TestCase):
    def test_read(self):
        readConfig = ReadComponentConfig()
        file = cStringIO.StringIO(sample_cmp_cfg)
        expected = {'addWeight': 1.0, 'efficiency': 'CFG: eff', 'triggers': [], 'xSection': 28730000}
        self.assertEqual(expected, readConfig._readImp(file))

##____________________________________________________________________________||
