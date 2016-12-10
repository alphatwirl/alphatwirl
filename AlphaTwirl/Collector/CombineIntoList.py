# Tai Sakuma <tai.sakuma@cern.ch>

from functions import *

##__________________________________________________________________||
def countsToList(counts, sort = True):
    try: # for Scan
        d = [ ]
        for k, summary in counts.iteritems():
            for v in summary.contents:
                d.append(k + tuple(v))
    except TypeError: # for Count, etc, need to be unified
        d = [k + tuple(v.contents) for k, v in counts.iteritems()]
    if sort: d.sort()
    return d

##__________________________________________________________________||
def combinedToList(combined, columns, sort = True):
    d = [ ]
    for datasetName, summarizer in combined.iteritems():
        l = countsToList(summarizer.results(), sort)
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
        dataset_summarizer_pairs = [[d, r.results()] for d, r in datasetReaderPairs]
        combined = add_summarizers_for_the_same_dataset(dataset_summarizer_pairs)
        return combinedToList(combined, (self.datasetColumnName, ) + self.keyNames + self.valNames, self.sort)

##__________________________________________________________________||
