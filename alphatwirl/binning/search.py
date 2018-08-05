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
