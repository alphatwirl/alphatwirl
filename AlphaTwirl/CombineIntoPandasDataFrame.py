# Tai Sakuma <sakuma@fnal.gov>
import AlphaTwirl
import pandas

##____________________________________________________________________________||
class CombineIntoPandasDataFrame(object):
    def __init__(self):
        self.datasetColumnName = 'component'

    def combine(self, datasetReaderPairs):
        df = pandas.DataFrame()
        for datasetName, reader in datasetReaderPairs:
            tbl_c = AlphaTwirl.countsToDataFrame(reader.results(), reader.keynames())
            tbl_c.insert(0, self.datasetColumnName, datasetName)
            df = df.append(tbl_c)
        return df

##____________________________________________________________________________||
