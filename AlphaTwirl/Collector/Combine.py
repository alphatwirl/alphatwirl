# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class Combine(object):
    def combine(self, datasetReaderPairs):
        combined = { }
        for datasetName, reader in datasetReaderPairs:
            summarizer = reader.results()
            if not summarizer: continue
            if datasetName in combined:
                combined[datasetName] = combined[datasetName] + summarizer
            else:
                combined[datasetName] = summarizer
        return combined

##__________________________________________________________________||
