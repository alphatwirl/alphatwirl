# Tai Sakuma <tai.sakuma@cern.ch>

from Combine import Combine

##__________________________________________________________________||
def countsToList(counts):
    d = [k + tuple(v) for k, v in counts.iteritems()]
    d.sort()
    return d

##__________________________________________________________________||
def combinedToList(combined, columns):
    d = [ ]
    for datasetName, count in combined.iteritems():
        l = countsToList(count.results())
        d.extend([(datasetName, ) + e for e in l])
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
        return combinedToList(combined, (self.datasetColumnName, ) + self.keyNames + self.valNames)

##__________________________________________________________________||
