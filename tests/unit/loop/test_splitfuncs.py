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

def test_apply_max_events_total():

    # simple
    file_nevents_list = [('A', 100), ('B', 100)]
    max_events_total = 120
    expected = [('A', 100), ('B', 20)]
    assert expected == _apply_max_events_total(file_nevents_list, max_events_total)

    # exact
    file_nevents_list = [('A', 100), ('B', 200)]
    max_events_total = 300
    expected = [('A', 100), ('B', 200)]
    assert expected == _apply_max_events_total(file_nevents_list, max_events_total)

    # zero
    file_nevents_list = [('A', 100), ('B', 200)]
    max_events_total = 0
    expected = [ ]
    assert expected == _apply_max_events_total(file_nevents_list, max_events_total)

    # empty
    file_nevents_list = [ ]
    max_events_total = 10
    expected = [ ]
    assert expected == _apply_max_events_total(file_nevents_list, max_events_total)

##__________________________________________________________________||
