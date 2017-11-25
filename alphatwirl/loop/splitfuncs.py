# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def create_file_start_length_list(file_nevents_list, max_events_per_run = -1, max_events_total = -1, max_files_per_run = 1):

    file_nevents_list = _apply_max_events_total(file_nevents_list, max_events_total)

    return _file_start_length_list(file_nevents_list, max_events_per_run, max_files_per_run)

##__________________________________________________________________||
def _apply_max_events_total(file_nevents_list, max_events_total = -1):

    if max_events_total < 0: return file_nevents_list

    ret = [ ]
    for file, nevents in file_nevents_list:
        if max_events_total == 0: break
        nevents = min(max_events_total, nevents)
        ret.append((file, nevents))
        max_events_total -= nevents
    return ret

##__________________________________________________________________||
def _file_start_length_list(file_nevents_list, max_events_per_run, max_files_per_run):

    if not file_nevents_list:
        return [ ]

    total_nevents = sum([n for f, n, in file_nevents_list])
    if total_nevents == 0:
        return [ ]

    if max_files_per_run == 0:
        return [ ]

    if max_events_per_run == 0:
        return [ ]

    if max_events_per_run < 0:
        max_events_per_run = total_nevents

    total_nfiles = len(set([f for f, n, in file_nevents_list]))
    if max_files_per_run < 0:
        max_files_per_run = total_nfiles


    files = [ ]
    nevents = [ ]
    start = [ ]
    length = [ ]
    i = 0
    for file_, nev in file_nevents_list:

        if nev == 0:
            continue

        if i == len(files):
            # create a new run
            files.append([ ])
            nevents.append(0)
            start.append(0)
            length.append(0)

        files[i].append(file_)
        nevents[i] += nev

        if max_events_per_run >= nevents[i]:
            length[i] = nevents[i]

        else:
            dlength = max_events_per_run - length[i]
            length[i] = max_events_per_run

            i += 1
            files.append([file_])
            nevents.append(nevents[i-1] - length[i-1])
            start.append(dlength)

            while max_events_per_run < nevents[i]:
                length.append(max_events_per_run)

                i += 1
                files.append([file_])
                nevents.append(nevents[i-1] - length[i-1])
                start.append(start[i-1] + length[i-1])

            length.append(nevents[i])

        if max_events_per_run == nevents[i]:
            i += 1 # to next run
            continue

        if max_files_per_run == len(files[i]):
            i += 1 # to next run

    # print files, nevents, start, length
    ret = list(zip(files, start, length))

    return ret

##__________________________________________________________________||
def _start_length_pairs_for_split_lists(ntotal, max_per_list):
    # e.g., ntotal =  35, max_per_list = 10

    if max_per_list < 0: return [(0, ntotal)]

    nlists = ntotal//max_per_list
    # https://stackoverflow.com/questions/1282945/python-integer-division-yields-float
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
