# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def start_length_pairs_for_split_lists(ntotal, max_per_list):
    # e.g., ntotal =  35, max_per_list = 10

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
def minimum_positive_value(vals):
    # returns -1 if all negative or empty
    vals = [v for v in vals if v >= 0]
    if not vals: return -1
    return min(vals)

##__________________________________________________________________||
