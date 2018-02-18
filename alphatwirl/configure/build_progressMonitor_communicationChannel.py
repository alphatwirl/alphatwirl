# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.misc.deprecation import atdeprecated
from alphatwirl.parallel.build import build_parallel_multiprocessing

##__________________________________________________________________||
@atdeprecated(msg='use alphatwirl.parallel.build.build_parallel_multiprocessing() instead.')
def build_progressMonitor_communicationChannel(quiet, processes):
    parallel = build_parallel_multiprocessing(quiet, processes)
    return parallel.progressMonitor, parallel.communicationChannel

##__________________________________________________________________||
