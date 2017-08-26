import unittest

from alphatwirl.heppyresult import TblBranch

##__________________________________________________________________||
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
