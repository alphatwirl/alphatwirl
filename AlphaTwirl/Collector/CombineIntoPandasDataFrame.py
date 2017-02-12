# Tai Sakuma <tai.sakuma@cern.ch>

import pandas

##__________________________________________________________________||
def combinedToDataFrame(combined, columns):
    l = combinedToList(combined, columns)
    l = l[1:] # remove the column header
    return pandas.DataFrame(l, columns = columns)

##__________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self, keyNames, valNames):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames
        self.valNames = valNames

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combine = Combine()
        combined = combine.combine(datasetReaderPairs)
        return combinedToDataFrame(combined, (self.datasetColumnName, ) + self.keyNames + self.valNames)

##__________________________________________________________________||
