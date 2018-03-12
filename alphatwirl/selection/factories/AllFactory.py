# Tai Sakuma <tai.sakuma@gmail.com>
from .FactoryDispatcher import call_factory

##__________________________________________________________________||
def AllFactory(path_cfg_list, name=None,  **kargs):

    ret = kargs['AllClass'](name=name)

    for path_cfg in path_cfg_list:
        ret.add(call_factory(path_cfg, **kargs))

    return ret

##__________________________________________________________________||
