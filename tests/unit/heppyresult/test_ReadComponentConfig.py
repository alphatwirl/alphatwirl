from alphatwirl.heppyresult import ReadComponentConfig
import unittest
import io
import os

##__________________________________________________________________||
sample_cmp_cfg = b"""MCComponent: QCD_HT_100To250_Chunk0
	addWeight      :   1.0
	efficiency     :   CFG: eff
	triggers       :   []
	xSection       :   28730000
"""

##__________________________________________________________________||
def mock_isfile(path): return False

##__________________________________________________________________||
class TestReadComponentConfig(unittest.TestCase):
    def test_read(self):
        readConfig = ReadComponentConfig()
        file = io.BytesIO(sample_cmp_cfg)
        expected = {b'addWeight': 1.0, b'efficiency': b'CFG: eff', b'triggers': [], b'xSection': 28730000}
        self.assertEqual(expected, readConfig._readImp(file))

    @unittest.skip("skip because of logging. assertLogs can be used here for Python 3.4")
    def test_no_file(self):
        isfile_org = os.path.isfile
        os.path.isfile = mock_isfile

        readConfig = ReadComponentConfig()
        self.assertIsNone(readConfig('config.txt'))

        os.path.isfile = isfile_org

##__________________________________________________________________||
