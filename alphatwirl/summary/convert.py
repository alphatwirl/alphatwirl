# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

##__________________________________________________________________||
def convert_key_vals_dict_to_tuple_list(dict_, fill=float('nan')):

    d = [ ]

    if not dict_: return d

    vlen = max([len(vs) for vs in itertools.chain(*dict_.values())])

    for k, vs in dict_.items():
        try:
            d.extend([k + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])
        except TypeError:
            # assume k is not a tuple
            d.extend([(k, ) + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])


    return d

##__________________________________________________________________||
