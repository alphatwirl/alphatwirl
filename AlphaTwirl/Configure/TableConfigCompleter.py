# Tai Sakuma <tai.sakuma@cern.ch>
import os

##____________________________________________________________________________||
class WeightCalculatorOne(object):
    def __call__(self, event):
        return 1.0

##__________________________________________________________________||
def createOutFileName(columnNames, indices, prefix = 'tbl_component_', suffix = '.txt'):
    # for example, if columnNames = ('var1', 'var2', 'var3') and indices = (1, None, 2),
    # l will be ['var1', '1', 'var2', 'var3', '2']
    l = columnNames if indices is None else [str(e) for sublist in zip(columnNames, indices) for e in sublist if e is not None]
    ret = prefix + '_'.join(l) + suffix # e.g. "tbl_component_var1_1_var2_var3_2.txt"
    return ret

##__________________________________________________________________||
class TableConfigCompleter(object):
    def __init__(self, defaultCountsClass, outDir):
        self.defaultCountsClass = defaultCountsClass
        self.outDir = outDir

    def complete(self, tblcfg):
        if 'outColumnNames' not in tblcfg: tblcfg['outColumnNames'] = tblcfg['branchNames']
        if 'indices' not in tblcfg: tblcfg['indices'] = None
        if 'countsClass' not in tblcfg: tblcfg['countsClass'] = self.defaultCountsClass
        if 'outFile' not in tblcfg: tblcfg['outFile'] = True
        if 'weight' not in tblcfg: tblcfg['weight'] = WeightCalculatorOne()
        if tblcfg['outFile']:
            if 'outFileName' not in tblcfg: tblcfg['outFileName'] = createOutFileName(tblcfg['outColumnNames'], tblcfg['indices'])
            if 'outFilePath' not in tblcfg: tblcfg['outFilePath'] = os.path.join(self.outDir, tblcfg['outFileName'])
            return tblcfg

##__________________________________________________________________||
