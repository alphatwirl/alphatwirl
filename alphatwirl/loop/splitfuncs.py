# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def create_file_start_length_list(file_nevents_list, max_per_run = -1, max_total = -1):

    file_nevents_list = _apply_max_total(file_nevents_list, max_total)

    ret = [ ]
    for file, nevents in file_nevents_list:
        start_length_pairs = _start_length_pairs_for_split_lists(nevents, max_per_run)
        for start, length in start_length_pairs:
            ret.append((file, start, length))
    return ret

##__________________________________________________________________||
def _apply_max_total(file_nevents_list, max_total = -1):

    if max_total < 0: return file_nevents_list

    ret = [ ]
    for file, nevents in file_nevents_list:
        if max_total == 0: break
        nevents = min(max_total, nevents)
        ret.append((file, nevents))
        max_total -= nevents
    return ret

##__________________________________________________________________||
def _start_length_pairs_for_split_lists(ntotal, max_per_list):
    # e.g., ntotal =  35, max_per_list = 10

    if max_per_list < 0: return [(0, ntotal)]

    nlists = ntotal/max_per_list
    # nlists = 3

    ret = [(i*max_per_list, max_per_list) for i in range(nlists)]
    # e.g., [(0, 10), (10, 10), (20, 10)]

    remainder =  ntotal % max_per_list
    # e.g., 5

    if remainder > 0:
        last = (nlists*max_per_list, remainder)
        # e.g, (30, 5)

        ret.append(last)

    # e.g., [(0, 10), (10, 10), (20, 10), (30, 5)]
    return ret

##__________________________________________________________________||
def _minimum_positive_value(vals):
    # returns -1 if all negative or empty
    vals = [v for v in vals if v >= 0]
    if not vals: return -1
    return min(vals)

##__________________________________________________________________||
