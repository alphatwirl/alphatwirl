# Tai Sakuma <tai.sakuma@gmail.com>
from .FactoryDispatcher import call_factory

##__________________________________________________________________||
def AnyFactory(path_cfg_list, name=None,  **kargs):

    ret = kargs['AnyClass'](name=name)

    for path_cfg in path_cfg_list:
        ret.add(call_factory(path_cfg, **kargs))

    return ret

##__________________________________________________________________||
