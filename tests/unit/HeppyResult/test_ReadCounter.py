from AlphaTwirl.HeppyResult import ReadCounter
import unittest
import collections
import cStringIO
import os

##____________________________________________________________________________||
sample_counts_txt = """Counter SkimReport :
	 All Events                                  500000 	 1.00 	 1.0000
	 Sum Weights                              1042218.60703 	 2.08 	 2.0844


"""

##____________________________________________________________________________||
def mock_isfile(path): return False

##____________________________________________________________________________||
class TestReadCounter(unittest.TestCase):

    def test_read_file(self):
        readConfig = ReadCounter()
        file = cStringIO.StringIO(sample_counts_txt)
        expected = collections.OrderedDict([('All Events', {'count': 500000.0, 'eff2': 1.0, 'eff1': 1.0}), ('Sum Weights', {'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08})])
        self.assertEqual(expected, readConfig._readImp(file))

    def test_no_file(self):
        isfile_org = os.path.isfile
        os.path.isfile = mock_isfile

        readConfig = ReadCounter()
        self.assertIsNone(readConfig('SkimReport.txt'))

        os.path.isfile = isfile_org

    def test_readLine(self):
        readConfig = ReadCounter()

        line = "	 Sum Weights                              1042218.60703 	 2.08 	 2.0844"
        level, content = readConfig._readLine(line)
        self.assertEqual('Sum Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

    def test_readLine_tab_in_level(self):
        readConfig = ReadCounter()

        line = "	 Sum 	 Weights                              1042218.60703 	 2.08 	 2.0844"
        level, content = readConfig._readLine(line)
        self.assertEqual('Sum \t Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

    def test_readLine_tab_(self):
        readConfig = ReadCounter()

        line = "\t Sum \t Weights                              1042218.60703 \t 2.08 \t 2.0844"
        level, content = readConfig._readLine(line)
        self.assertEqual('Sum \t Weights', level)
        self.assertEqual({'count': 1042218.60703, 'eff2': 2.0844, 'eff1': 2.08}, content)

##____________________________________________________________________________||
