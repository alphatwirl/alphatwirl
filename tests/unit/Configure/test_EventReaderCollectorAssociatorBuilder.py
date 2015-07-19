from AlphaTwirl.Configure import EventReaderCollectorAssociatorBuilder
import unittest

##__________________________________________________________________||
class MockCounts: pass

##__________________________________________________________________||
class MockWeight: pass

##__________________________________________________________________||
class MockBinning: pass

##__________________________________________________________________||
class TestEventReaderCollectorAssociatorBuilder(unittest.TestCase):

    def test_one(self):
        builder = EventReaderCollectorAssociatorBuilder()
        tblcfg = {
            'binnings': (MockBinning(),),
            'weight': MockWeight(),
            'outFileName': 'tbl_component_met_pt.txt',
            'branchNames': ('met_pt',),
            'countsClass': MockCounts,
            'outFilePath': '/tmp/tbl_component_met_pt.txt',
            'outFile': True,
            'outColumnNames': ('met_pt',),
            'indices': None
        }

        builder.build(tblcfg)

##__________________________________________________________________||
