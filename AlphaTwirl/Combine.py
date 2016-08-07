# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class Combine(object):
    def combine(self, datasetReaderPairs):
        combined = { }
        for datasetName, reader in datasetReaderPairs:
            result = reader.results()
            if not result: continue
            if datasetName in combined:
                combined[datasetName] = combined[datasetName] + result
            else:
                combined[datasetName] = result
        return combined

##__________________________________________________________________||
