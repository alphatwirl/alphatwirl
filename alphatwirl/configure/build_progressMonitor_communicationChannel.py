# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.misc.deprecation import atdeprecated
from alphatwirl.parallel.build import build_parallel

##__________________________________________________________________||
@atdeprecated(msg='use alphatwirl.parallel.build.build_parallel() instead.')
def build_progressMonitor_communicationChannel(quiet, processes):
    parallel = build_parallel(
        parallel_mode='multiprocessing',
        quiet=quiet, processes=processes
    )
    return parallel.progressMonitor, parallel.communicationChannel

##__________________________________________________________________||
