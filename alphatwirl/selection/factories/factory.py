# Tai Sakuma <tai.sakuma@gmail.com>

from .expand import expand_path_cfg

##__________________________________________________________________||
def AllFactory(components, name=None, **kargs):
    ret = kargs['AllClass'](name=name)
    for path_cfg in components:
        ret.add(call_factory(path_cfg, **kargs))
    return ret

def AnyFactory(components, name=None,  **kargs):
    ret = kargs['AnyClass'](name=name)
    for path_cfg in components:
        ret.add(call_factory(path_cfg, **kargs))
    return ret

def NotFactory(path_cfg, name=None,  **kargs):
    return kargs['NotClass'](selection=call_factory(path_cfg, **kargs), name=name)

##__________________________________________________________________||
def LambdaStrFactory(lambda_str, LambdaStrClass, name=None, **kargs):
    return LambdaStrClass(lambda_str=lambda_str.format(**kargs), name=name)

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

    ret_dict = dict(
        AllFactory=AllFactory,
        AnyFactory=AnyFactory,
        NotFactory=NotFactory,
        LambdaStrFactory=LambdaStrFactory,
    )

    return ret_dict[name]

##__________________________________________________________________||
