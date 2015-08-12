# Tai Sakuma <tai.sakuma@cern.ch>
import os
from .TableFileNameComposer import TableFileNameComposer
from ..Counter import Counts, WeightCalculatorOne

##__________________________________________________________________||
class TableConfigCompleter(object):
    """
    an example complete config::

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

    """
    def __init__(self,
                 defaultCountsClass = Counts,
                 defaultWeight = WeightCalculatorOne(),
                 defaultOutDir = '.',
                 createOutFileName = TableFileNameComposer()):

        self.defaultCountsClass = defaultCountsClass
        self.defaultWeight = defaultWeight
        self.defaultOutDir = defaultOutDir
        self.createOutFileName = createOutFileName

    def complete(self, tblcfg):
        ret = tblcfg.copy()
        if 'outColumnNames' not in ret: ret['outColumnNames'] = ret['branchNames']
        if 'indices' not in ret: ret['indices'] = None
        if 'countsClass' not in ret: ret['countsClass'] = self.defaultCountsClass
        if 'outFile' not in ret: ret['outFile'] = True
        if 'weight' not in ret: ret['weight'] = self.defaultWeight
        if ret['outFile']:
            if 'outFileName' not in ret: ret['outFileName'] = self.createOutFileName(ret['outColumnNames'], ret['indices'])
            if 'outFilePath' not in ret: ret['outFilePath'] = os.path.join(self.defaultOutDir, ret['outFileName'])
            return ret

##__________________________________________________________________||
