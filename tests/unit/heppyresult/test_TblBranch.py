import unittest

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.heppyresult import TblBranch

##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestTblBranch(unittest.TestCase):

    def setUp(self):
        self.obj = TblBranch(
            analyzerName = 'roctree',
            fileName = 'tree.root',
            treeName = 'tree',
            outPath = 'tbl_out',
            addType = True,
            addSize = False,
            addTitle = False,
            sortBySize = False
        )

    def test_read(self):
        self.obj.begin()

##__________________________________________________________________||
