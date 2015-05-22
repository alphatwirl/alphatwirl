# Tai Sakuma <tai.sakuma@cern.ch>

from Combine import Combine

##____________________________________________________________________________||
def countsToList(counts, keyNames):
    valNames = counts.values()[0].keys()
    d = [k + tuple([v[n] for n in valNames]) for k, v in counts.iteritems()]
    d.sort()
    columns = tuple(keyNames) + tuple(valNames)
    d.insert(0, columns)
    return d

##____________________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combine = Combine()
        combined = combine.combine(datasetReaderPairs)
        reader = datasetReaderPairs[0][1]
        if len(combined) == 0:
            columns = (self.datasetColumnName, ) + tuple(self.keyNames) + tuple(reader.valNames())
            return [columns]
        return countsToList(combined, (self.datasetColumnName, ) + self.keyNames)

##____________________________________________________________________________||
