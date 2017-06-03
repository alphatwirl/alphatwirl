# Tai Sakuma <tai.sakuma@cern.ch>
import itertools

##__________________________________________________________________||
def convert_key_vals_dict_to_tuple_list(dict_, fill = float('nan'), sort = True):

    d = [ ]

    if not dict_: return d

    vlen = max([len(vs) for vs in itertools.chain(*dict_.values())])

    for k, vs in dict_.iteritems():
        d.extend([k + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])

    if sort: d.sort()

    return d

##__________________________________________________________________||
