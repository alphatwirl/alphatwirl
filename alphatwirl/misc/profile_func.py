# Tai Sakuma <tai.sakuma@cern.ch>
from __future__ import print_function
import cProfile, pstats
from io import StringIO, BytesIO

##__________________________________________________________________||
def print_profile_func(func, profile_out_path=None):
    result = profile_func(func)
    if profile_out_path is None:
        print(result)
    else:
        with open(profile_out_path, 'w') as f:
            f.write(result)

##__________________________________________________________________||
def profile_func(func):
    pr = cProfile.Profile()
    pr.enable()
    func()
    pr.disable()
    sortby = 'cumulative'
    try:
        s = StringIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    except TypeError:
        s = BytesIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    return s.getvalue()

##__________________________________________________________________||
