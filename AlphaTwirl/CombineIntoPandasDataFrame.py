# Tai Sakuma <sakuma@fnal.gov>
import pandas

##____________________________________________________________________________||
def countsToDataFrame(counts, keyNames, valNames = ('n', 'nvar')):
    columns = tuple(keyNames) + tuple(valNames)
    if not counts:
        return pandas.DataFrame(columns = columns)
        return
    d = [k + (v[valNames[0]], v[valNames[1]]) for k, v in counts.iteritems()]
    d.sort()
    return pandas.DataFrame(d, columns = columns)

##____________________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self):
        self.datasetColumnName = 'component'

    def combine(self, datasetReaderPairs):
        df = pandas.DataFrame()
        for datasetName, reader in datasetReaderPairs:
            tbl_c = countsToDataFrame(reader.results(), reader.keynames())
            tbl_c.insert(0, self.datasetColumnName, datasetName)
            df = df.append(tbl_c, ignore_index = True)
        return df

##____________________________________________________________________________||
