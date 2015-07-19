# Tai Sakuma <tai.sakuma@cern.ch>
import os
from .TableFileNameComposer import TableFileNameComposer

##__________________________________________________________________||
class TableConfigCompleter(object):
    def __init__(self, defaultCountsClass, defaultWeight, outDir):
        self.defaultCountsClass = defaultCountsClass
        self.defaultWeight = defaultWeight
        self.createOutFileName = TableFileNameComposer()
        self.outDir = outDir

    def complete(self, tblcfg):
        ret = tblcfg.copy()
        if 'outColumnNames' not in ret: ret['outColumnNames'] = ret['branchNames']
        if 'indices' not in ret: ret['indices'] = None
        if 'countsClass' not in ret: ret['countsClass'] = self.defaultCountsClass
        if 'outFile' not in ret: ret['outFile'] = True
        if 'weight' not in ret: ret['weight'] = self.defaultWeight
        if ret['outFile']:
            if 'outFileName' not in ret: ret['outFileName'] = self.createOutFileName(ret['outColumnNames'], ret['indices'])
            if 'outFilePath' not in ret: ret['outFilePath'] = os.path.join(self.outDir, ret['outFileName'])
            return ret

##__________________________________________________________________||
