# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

##__________________________________________________________________||
def key_vals_dict_to_tuple_list(key_vals_dict, fill=float('nan')):

    tuple_list = [ ]

    if not key_vals_dict: return tuple_list

    vlen = max([len(vs) for vs in itertools.chain(*key_vals_dict.values())])

    for k, vs in key_vals_dict.items():
        try:
            tuple_list.extend([k + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])
        except TypeError:
            # assume k is not a tuple
            tuple_list.extend([(k, ) + tuple(v) + (fill, )*(vlen - len(v)) for v in vs])


    return tuple_list

##__________________________________________________________________||
