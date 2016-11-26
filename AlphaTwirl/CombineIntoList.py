# Tai Sakuma <tai.sakuma@cern.ch>

from Combine import Combine

##__________________________________________________________________||
def countsToList(counts, sort = True):
    try:
        d = [k + tuple(v) for k, v in counts.iteritems()]
        if sort: d.sort()
    except AttributeError:
        # assume counts is already a list
        d = counts
    return d

##__________________________________________________________________||
def combinedToList(combined, columns, sort = True):
    d = [ ]
    for datasetName, count in combined.iteritems():
        l = countsToList(count.results(), sort)
        d.extend([(datasetName, ) + e for e in l])
    if sort: d.sort()
    d.insert(0, columns)
    return d

##__________________________________________________________________||
class CombineIntoList(object):
    def __init__(self, keyNames, valNames, sort = True):
        self.datasetColumnName = 'component'
        self.keyNames = keyNames
        self.valNames = valNames
        self.sort = sort

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combine = Combine()
        combined = combine.combine(datasetReaderPairs)
        return combinedToList(combined, (self.datasetColumnName, ) + self.keyNames + self.valNames, self.sort)

##__________________________________________________________________||
