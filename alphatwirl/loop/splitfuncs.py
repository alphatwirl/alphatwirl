# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def create_files_start_length_list(
        files, func_get_nevents_in_file=None,
        max_events=-1, max_events_per_run=-1,
        max_files=-1, max_files_per_run=1):

    files = _apply_max_files(files, max_files)

    if max_events == 0 or max_events_per_run == 0:
        return [ ]

    if max_events < 0 and max_events_per_run < 0:
        return _fast_path(files, max_files_per_run)

    return _full_path(files, func_get_nevents_in_file, max_events,
                           max_events_per_run, max_files_per_run)

##__________________________________________________________________||
def _apply_max_files(files, max_files):
    if max_files < 0:
        return files
    return files[:min(max_files, len(files))]

def _fast_path(files, max_files_per_run):
    if not files:
        return [ ]
    if max_files_per_run < 0:
        return [(files, 0, -1)]
    if max_files_per_run == 0:
        return [ ]
    return [(files[i:(i + max_files_per_run)], 0, -1) for i in range(0, len(files), max_files_per_run)]

def _full_path(files, func_get_nevents_in_file, max_events, max_events_per_run, max_files_per_run):

    if max_events == 0 or max_events_per_run == 0 or max_files_per_run == 0:
        return [ ]

    # this can be slow
    file_nevents_list = _file_nevents_list(
        files,
        func_get_nevents_in_file=func_get_nevents_in_file,
        max_events=max_events
    )

    file_nevents_list = _apply_max_events_total(
        file_nevents_list, max_events
    )

    files_start_length_list = _files_start_length_list(
        file_nevents_list, max_events_per_run, max_files_per_run
    )

    return files_start_length_list

def _file_nevents_list(files, func_get_nevents_in_file, max_events):
    total_events = 0
    ret = [ ]
    for f in files:
        if 0 <= max_events <= total_events:
            break

        # this can be slow
        n = func_get_nevents_in_file(f)

        if n is None:
            continue

        if n == 0:
            continue

        ret.append((f, n))
        total_events += n
    return ret

def _apply_max_events_total(file_nevents_list, max_events_total):

    if max_events_total < 0:
        return file_nevents_list

    ret = [ ]
    for file, nevents in file_nevents_list:
        if max_events_total == 0:
            break
        nevents = min(max_events_total, nevents)
        ret.append((file, nevents))
        max_events_total -= nevents
    return ret

##__________________________________________________________________||
def _files_start_length_list(file_nevents_list, max_events_per_run, max_files_per_run):

    if not file_nevents_list:
        return [ ]

    if max_events_per_run == 0 or max_files_per_run == 0:
        return [ ]

    total_nevents = sum([n for f, n, in file_nevents_list])
    if total_nevents == 0:
        return [ ]

    if max_events_per_run < 0:
        max_events_per_run = total_nevents

    total_nfiles = len(set([f for f, n, in file_nevents_list]))
    if max_files_per_run < 0:
        max_files_per_run = total_nfiles

    ##
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

    return list(zip(files, start, length))

##__________________________________________________________________||
