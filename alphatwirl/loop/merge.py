# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def merge_in_order(map_, id_, data):

    ## merge to prev
    idx = list(map_.keys()).index(id_)
    idx_prev = idx - 1
    if idx_prev < 0:
        map_[id_] = data
    else:
        data_prev = list(map_.values())[idx_prev]
        id_prev = list(map_.keys())[idx_prev]
        if data_prev is None:
            map_[id_] = data
        else:
            if hasattr(data_prev, 'merge'):
                data_prev.merge(data)
            map_.pop(id_)
            id_ = id_prev
            data = data_prev

    ## merge next
    idx = list(map_.keys()).index(id_)
    idx_next = idx + 1
    if idx_next < len(map_):
        data_next = list(map_.values())[idx_next]
        if data_next is not None:
            if hasattr(data, 'merge'):
                data.merge(data_next)
            map_.pop(list(map_.keys())[idx_next])

##__________________________________________________________________||
