# Tai Sakuma <tai.sakuma@gmail.com>

from alphatwirl.loop.splitfuncs import *
from alphatwirl.loop.splitfuncs import _apply_max_events_total
from alphatwirl.loop.splitfuncs import _file_start_length_list

##__________________________________________________________________||
def test_create_file_start_length_list():

    # simple
    file_nevents_list = [('A', 100), ('B', 100)]
    max_events_per_run = 30
    max_events_total = 140
    max_files_per_run = 2

    expected = [
        (['A'], 0, 30), (['A'], 30, 30), (['A'], 60, 30), (['A', 'B'], 90, 30),
        (['B'], 20, 20)
    ]
    assert expected == create_file_start_length_list(file_nevents_list, max_events_per_run, max_events_total, max_files_per_run)

##__________________________________________________________________||
