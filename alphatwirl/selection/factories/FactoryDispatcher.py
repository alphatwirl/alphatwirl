# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def FactoryDispatcher(path_cfg, **kargs):

    alias_dict = kargs['aliasDict'] if 'aliasDict' in kargs else None
    path_cfg = expand_path_cfg(path_cfg, alias_dict=alias_dict)

    if not isinstance(path_cfg, dict):
        raise ValueError("cannot recognize the path_cfg")

    if 'factory' not in path_cfg:
        raise ValueError("cannot recognize the path_cfg")

    path_cfg_copy = path_cfg.copy()
    factoryName = path_cfg_copy.pop('factory')
    factory = find_factory(factoryName)
    kargs_copy = kargs.copy()
    kargs_copy.update(path_cfg_copy)

    return factory(**kargs_copy)

##__________________________________________________________________||
def expand_path_cfg(path_cfg, alias_dict=None, overriding_kargs=dict()):

    if isinstance(path_cfg, str):
        return _expand_path_cfg_str(path_cfg, alias_dict, overriding_kargs)

    if isinstance(path_cfg, dict):
        return _expand_path_cfg_dict(path_cfg, alias_dict)

    # assume tuple or list
    return _expand_path_cfg_tuple(path_cfg, alias_dict, overriding_kargs)

##__________________________________________________________________||
def _expand_path_cfg_str(path_cfg, alias_dict, overriding_kargs):

    if alias_dict is not None and path_cfg in alias_dict:
        new_overriding_kargs = dict(alias=path_cfg)
        new_overriding_kargs.update(overriding_kargs)
        return expand_path_cfg(
            alias_dict[path_cfg],
            alias_dict=alias_dict,
            overriding_kargs=new_overriding_kargs
        )

    ret = dict(factory='LambdaStrFactory', lambda_str=path_cfg)

    overriding_kargs_copy = overriding_kargs.copy()
    if 'alias' in overriding_kargs:
        ret['name'] = overriding_kargs_copy.pop('alias')

    if 'name' in overriding_kargs:
        ret['name'] = overriding_kargs_copy.pop('name')

    ret.update(overriding_kargs_copy)
    return ret

##__________________________________________________________________||
def _expand_path_cfg_dict(path_cfg, alias_dict):
    if 'factory' in path_cfg:
        return path_cfg

    if not sum([k in path_cfg for k in ('All', 'Any', 'Not')]) <= 1:
        raise ValueError("Any pair of 'All', 'Any', 'Not' cannot be simultaneously given unless factory is given!")

    if 'All' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'AllFactory'
        new_path_cfg['path_cfg_list'] = new_path_cfg.pop('All')
        return new_path_cfg

    if 'Any' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'AnyFactory'
        new_path_cfg['path_cfg_list'] = new_path_cfg.pop('Any')
        return new_path_cfg

    if 'Not' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'NotFactory'
        new_path_cfg['path_cfg'] = new_path_cfg.pop('Not')
        return new_path_cfg

    raise ValueError("cannot recognize the path_cfg")

##__________________________________________________________________||
def _expand_path_cfg_tuple(path_cfg, alias_dict, overriding_kargs):

    if isinstance(path_cfg[0], str) and isinstance(path_cfg[1], dict):
        new_overriding_kargs = path_cfg[1].copy()
        new_overriding_kargs.update(overriding_kargs)
        return expand_path_cfg(
            path_cfg[0],
            overriding_kargs=new_overriding_kargs,
            alias_dict=alias_dict
        )

    raise ValueError("cannot recognize the path_cfg")

##__________________________________________________________________||
def find_factory(name):

    from .AllFactory import AllFactory
    from .AnyFactory import AnyFactory
    from .NotFactory import NotFactory
    from .LambdaStrFactory import LambdaStrFactory

    ret_dict = dict(
        AllFactory=AllFactory,
        AnyFactory=AnyFactory,
        NotFactory=NotFactory,
        LambdaStrFactory=LambdaStrFactory,
    )

    return ret_dict[name]

##__________________________________________________________________||
