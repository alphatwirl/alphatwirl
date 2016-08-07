# Tai Sakuma <tai.sakuma@cern.ch>

from Combine import Combine

##__________________________________________________________________||
def countsToList(counts, columns):
    d = [k + tuple(v) for k, v in counts.iteritems()]
    d.sort()
    d.insert(0, columns)
    return d

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames, valNames):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames
        self.valNames = valNames

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combine = Combine()
        combined = combine.combine(datasetReaderPairs)
        reader = datasetReaderPairs[0][1]
        if len(combined) == 0:
            columns = (self.datasetColumnName, ) + tuple(self.keyNames) + tuple(self.valNames)
            return [columns]
        return countsToList(combined, (self.datasetColumnName, ) + self.keyNames + self.valNames)

##__________________________________________________________________||
