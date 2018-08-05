# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def linear_search(val, boundaries):
    ret = 0
    for i, low in enumerate(boundaries):
        if low <= val:
            ret = i
        else:
            break
    return ret

##__________________________________________________________________||
def binary_search(val, boundaries):
    min_idx = 0
    max_idx = len(boundaries) - 1
    while min_idx <= max_idx:
        idx = min_idx + (max_idx - min_idx)//2
        low = boundaries[idx]
        if val == low:
            return idx
        up = boundaries[idx + 1]
        if val == up:
            return idx + 1
        if low < val < up:
            return idx
        elif up <= val:
            min_idx = idx
        else: # val < low
            max_idx = idx

##__________________________________________________________________||
