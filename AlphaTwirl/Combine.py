# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class Combine(object):
    def combine(self, datasetReaderPairs):
        combined = { }
        for datasetName, reader in datasetReaderPairs:
            counts = reader.results()
            if not counts: continue
            counts = dict([((datasetName, )+ k, v.copy()) for k, v in counts.iteritems()])
            combined.update(counts)
        return combined

##____________________________________________________________________________||
