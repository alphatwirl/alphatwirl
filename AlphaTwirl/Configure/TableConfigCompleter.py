# Tai Sakuma <tai.sakuma@cern.ch>
import os

##__________________________________________________________________||
class TableFileNameComposer(object):
    """Compose a name of a file to store the table from the column names and indices.


    For example, if column names are 'var1', 'var2', and 'var3' and
    indices are 1, None and 2, the file name will be
    'tbl_component_var1_1_var2_var3_2.txt'

    """
    def __call__(self, columnNames, indices, prefix = 'tbl_component_', suffix = '.txt'):
        # for example, if columnNames = ('var1', 'var2', 'var3') and indices = (1, None, 2),
        # l will be ['var1', '1', 'var2', 'var3', '2']
        l = columnNames if indices is None else [str(e) for sublist in zip(columnNames, indices) for e in sublist if e is not None]
        ret = prefix + '_'.join(l) + suffix # e.g. "tbl_component_var1_1_var2_var3_2.txt"
        return ret

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
