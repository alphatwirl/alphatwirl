# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def add_summarizers_for_the_same_dataset(dataset_summarizer_pairs):
    ret = { }
    for dataset, summarizer in dataset_summarizer_pairs:
        if not summarizer: continue
        if dataset in ret:
            ret[dataset] = ret[dataset] + summarizer
        else:
            ret[dataset] = summarizer
    return ret.items()

##__________________________________________________________________||
