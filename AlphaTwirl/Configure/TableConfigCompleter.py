# Tai Sakuma <tai.sakuma@cern.ch>
import os
from .TableFileNameComposer import TableFileNameComposer
from ..Summary import Count, WeightCalculatorOne

##__________________________________________________________________||
class TableConfigCompleter(object):
    """
    an example complete config::

        tblcfg = {
            'binnings': (MockBinning(),),
            'weight': MockWeight(),
            'outFileName': 'tbl_component_met_pt.txt',
            'keyAttrNames': ('met_pt',),
            'summaryClass': MockCounts,
            'outFilePath': '/tmp/tbl_component_met_pt.txt',
            'outFile': True,
            'keyOutColumnNames': ('met_pt',),
            'keyIndices': None
        }

    """
    def __init__(self,
                 defaultSummaryClass = Count,
                 defaultWeight = WeightCalculatorOne(),
                 defaultOutDir = '.',
                 createOutFileName = TableFileNameComposer()):

        self.defaultSummaryClass = defaultSummaryClass
        self.defaultWeight = defaultWeight
        self.defaultOutDir = defaultOutDir
        self.createOutFileName = createOutFileName

    def complete(self, tblcfg):
        ret = tblcfg.copy()
        if 'keyOutColumnNames' not in ret: ret['keyOutColumnNames'] = ret['keyAttrNames']
        if 'keyIndices' not in ret: ret['keyIndices'] = None
        if 'summaryClass' not in ret: ret['summaryClass'] = self.defaultSummaryClass
        if 'outFile' not in ret: ret['outFile'] = True
        if 'weight' not in ret: ret['weight'] = self.defaultWeight
        if ret['outFile']:
            if 'outFileName' not in ret: ret['outFileName'] = self.createOutFileName(ret['keyOutColumnNames'], ret['keyIndices'])
            if 'outFilePath' not in ret: ret['outFilePath'] = os.path.join(self.defaultOutDir, ret['outFileName'])
            return ret

##__________________________________________________________________||
