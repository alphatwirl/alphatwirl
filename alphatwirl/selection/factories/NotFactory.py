# Tai Sakuma <tai.sakuma@gmail.com>
from .FactoryDispatcher import call_factory

##__________________________________________________________________||
def NotFactory(path_cfg, name=None,  **kargs):
    return kargs['NotClass'](selection=call_factory(path_cfg, **kargs), name=name)

##__________________________________________________________________||
