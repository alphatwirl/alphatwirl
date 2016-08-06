# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class Combine(object):
    def combine(self, datasetReaderPairs):
        combined = { }
        for datasetName, reader in datasetReaderPairs:
            counts = reader.results()
            if not counts: continue
            counts = dict([((datasetName, ) + k, v.copy()) for k, v in counts.iteritems()])
            for k, v in counts.iteritems():
                if k not in combined:
                    combined[k] = v
                else:
                    combined[k] += v
        return combined

##__________________________________________________________________||
