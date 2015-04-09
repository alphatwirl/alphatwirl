# Tai Sakuma <tai.sakuma@cern.ch>
import pandas

##____________________________________________________________________________||
def countsToDataFrame(counts, keyNames):
    valNames = counts.values()[0].keys()
    d = [k + tuple([v[n] for n in valNames]) for k, v in counts.iteritems()]
    d.sort()
    columns = tuple(keyNames) + tuple(valNames)
    return pandas.DataFrame(d, columns = columns)

##____________________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self):
        self.datasetColumnName = 'component'

    def combine(self, datasetReaderPairs):
        if len(datasetReaderPairs) == 0: return None
        combined = { }
        for datasetName, reader in datasetReaderPairs:
            if not reader.results(): continue
            counts = reader.results()
            counts = dict([((datasetName, )+ k, v) for k, v in counts.iteritems()])
            combined.update(counts)
        if len(combined) == 0:
            reader = datasetReaderPairs[0][1]
            columns = (self.datasetColumnName, ) + tuple(reader.keynames()) + tuple(reader.valNames())
            return pandas.DataFrame(columns = columns)
        return countsToDataFrame(combined, (self.datasetColumnName, ) + reader.keynames())

##____________________________________________________________________________||
