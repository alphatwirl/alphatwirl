# Tai Sakuma <tai.sakuma@gmail.com>
from .FactoryDispatcher import FactoryDispatcher

##__________________________________________________________________||
def NotFactory(path_cfg, NotClass, name=None, **kargs):
    return NotClass(selection=FactoryDispatcher(path_cfg, **kargs), name=name)

##__________________________________________________________________||
