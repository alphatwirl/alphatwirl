from alphatwirl.heppyresult import ReadCounter
import unittest
import collections
import io
import os

##__________________________________________________________________||
sample_counts_txt = b"""Counter SkimReport :
	 All Events                                  500000 	 1.00 	 1.0000
	 Sum Weights                              1042218.60703 	 2.08 	 2.0844


"""

##__________________________________________________________________||
def mock_isfile(path): return False

##__________________________________________________________________||
class TestReadCounter(unittest.TestCase):

    def test_read_file(self):
        readCounter = ReadCounter()
        file = io.BytesIO(sample_counts_txt)
        expected = collections.OrderedDict([(b'All Events', {'count': 500000.0, 'eff2': 1.0, 'eff1': 1.0}), (b'Sum Weights', {'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08})])
        self.assertEqual(expected, readCounter._readImp(file))

    def test_no_file(self):
        isfile_org = os.path.isfile
        os.path.isfile = mock_isfile

        readCounter = ReadCounter()
        self.assertIsNone(readCounter('SkimReport.txt'))

        os.path.isfile = isfile_org

    def test_readLine(self):
        readCounter = ReadCounter()

        line = b"	 Sum Weights                              1042218.60703 	 2.08 	 2.0844"
        level, content = readCounter._readLine(line)
        self.assertEqual(b'Sum Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

    def test_readLine_tab_in_level(self):
        readCounter = ReadCounter()

        line = b"	 Sum 	 Weights                              1042218.60703 	 2.08 	 2.0844"
        level, content = readCounter._readLine(line)
        self.assertEqual(b'Sum \t Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

    def test_readLine_tab_(self):
        readCounter = ReadCounter()

        line = b"\t Sum \t Weights                              1042218.60703 \t 2.08 \t 2.0844"
        level, content = readCounter._readLine(line)
        self.assertEqual(b'Sum \t Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

    def test_readLine_scientific_notation(self):
        readCounter = ReadCounter()
        line = b"	 Sum Weights                              3.73134089883e+12 	 154498.74 	 154498.7447"
        level, content = readCounter._readLine(line)
        self.assertEqual(b'Sum Weights', level)
        self.assertEqual({'count': 3.73134089883e+12, 'eff2': 154498.7447, 'eff1': 154498.74}, content)

    def test_readLine_netative(self):
        readCounter = ReadCounter()
        line = b"	 too many objects after requirements         -848739 	 -1.00 	 -0.1717"
        level, content = readCounter._readLine(line)
        self.assertEqual(b'too many objects after requirements', level)
        self.assertEqual({'count': -848739, 'eff1': -1.0, 'eff2': -0.1717}, content)

##__________________________________________________________________||
