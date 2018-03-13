# Tai Sakuma <tai.sakuma@gmail.com>

from .expand import expand_path_cfg

##__________________________________________________________________||
def FactoryDispatcher(path_cfg, **kargs):

    alias_dict = kargs.get('aliasDict', { })
    path_cfg = expand_path_cfg(path_cfg, alias_dict=alias_dict)

    return call_factory(path_cfg, **kargs)

##__________________________________________________________________||
def call_factory(path_cfg, **kargs):

    path_cfg_copy = path_cfg.copy()
    factoryName = path_cfg_copy.pop('factory')
    factory = find_factory(factoryName)
    kargs_copy = kargs.copy()
    kargs_copy.update(path_cfg_copy)

    return factory(**kargs_copy)

##__________________________________________________________________||
def find_factory(name):

    from .factory import AllFactory
    from .factory import AnyFactory
    from .factory import NotFactory
    from .factory import LambdaStrFactory

    ret_dict = dict(
        AllFactory=AllFactory,
        AnyFactory=AnyFactory,
        NotFactory=NotFactory,
        LambdaStrFactory=LambdaStrFactory,
    )

    return ret_dict[name]

##__________________________________________________________________||
