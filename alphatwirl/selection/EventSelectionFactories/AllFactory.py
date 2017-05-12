# Tai Sakuma <tai.sakuma@cern.ch>
from .FactoryDispatcher import FactoryDispatcher

##__________________________________________________________________||
def AllFactory(path_cfg_list, name = None,  **kargs):

    ret = kargs['AllClass'](name = name)

    for path_cfg in path_cfg_list:
        ret.add(FactoryDispatcher(path_cfg, **kargs))

    return ret

##__________________________________________________________________||
