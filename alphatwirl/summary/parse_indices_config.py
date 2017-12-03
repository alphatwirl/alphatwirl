# Tai Sakuma <tai.sakuma@gmail.com>
import re

##__________________________________________________________________||
def parse_indices_config(indices):
    indices = list(indices)

    # indices e.g., [None, None, '(*)', '(*)', '\\1', '\\2']

    # replace None with 0
    indices = [0 if i is None else i for i in indices]
    # e.g., [0, 0, '(*)', '(*)', '\\1', '\\2']

    # search for elements in parentheses, e.g. '(*)'
    # at the momentum, only the asterisk '*' can be in the parentheses
    idxRefs = [re.search(r'^\((.*)\)$', i) if isinstance(i, str) else None for i in indices]
    # e.g., [None, None, <Match object>, <Match object>, None, None]

    # remove parentheses
    indices = [r.group(1) if r else i for i, r in zip(indices, idxRefs)]
    # e.g., [0, 0, '*', '*', '\\1', '\\2']

    ref = 1
    for i, v in enumerate(idxRefs):
        if v:
            idxRefs[i] = ref
            ref += 1
    # e.g., idxRefs  = [None, None, 1, 2, None, None]

    backrefIdxs = [int(i[1:]) if isinstance(i, str) and i.startswith('\\') else None for i in indices]
    # e.g., [None, None, None, None, 1, 2] # the original refs

    backrefIdxs = [None if i is None else idxRefs.index(i) for i in backrefIdxs]
    # e.g., [None, None, None, None, 2, 3] # indices in the list "indices"

    # e.g.:
    # backrefIdxs = [None, None, None, None, 2, 3]
    # indices = [0, 0, '*', '*', '\\1', '\\2']
    return backrefIdxs, indices

##__________________________________________________________________||
