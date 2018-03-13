# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def expand_path_cfg(path_cfg, alias_dict={ }, overriding_kargs={ }):

    if isinstance(path_cfg, str):
        return _expand_path_cfg_str(path_cfg, alias_dict, overriding_kargs)

    if isinstance(path_cfg, dict):
        return _expand_path_cfg_dict(path_cfg, alias_dict)

    # assume tuple or list
    return _expand_path_cfg_tuple(path_cfg, alias_dict, overriding_kargs)

##__________________________________________________________________||
def _expand_path_cfg_str(path_cfg, alias_dict, overriding_kargs):
    """expand a path config given as a string

    Args:
        path_cfg (str): to be given to lambda or an alias
        alias_dict (dict):
        overriding_kargs (dict):
    """


    if path_cfg in alias_dict:

        # e.g.,
        # path_cfg = 'var_cut'

        new_path_cfg = alias_dict[path_cfg]
        # e.g., ('ev : {low} <= ev.var[0] < {high}', {'low': 10, 'high': 200})

        new_overriding_kargs = dict(alias=path_cfg)
        # e.g., {'alias': 'var_cut'}

        new_overriding_kargs.update(overriding_kargs)
        # e.g., {'alias': 'var_cut', 'name': 'var_cut25', 'low': 25}

        return expand_path_cfg(
            new_path_cfg,
            alias_dict=alias_dict,
            overriding_kargs=new_overriding_kargs
        )

    # e.g.,
    # path_cfg = 'ev : {low} <= ev.var[0] < {high}'

    ret = dict(factory='LambdaStrFactory', lambda_str=path_cfg)
    # e.g.,
    # {
    #     'factory': 'LambdaStrFactory',
    #     'lambda_str': 'ev : {low} <= ev.var[0] < {high}'
    # }

    overriding_kargs_copy = overriding_kargs.copy()
    # e.g., {'low': 25, 'high': 200, 'alias': 'var_cut', 'name': 'var_cut25'}

    if 'alias' in overriding_kargs:
        ret['name'] = overriding_kargs_copy.pop('alias')

    if 'name' in overriding_kargs:
        ret['name'] = overriding_kargs_copy.pop('name')

    ret.update(overriding_kargs_copy)
    # e.g., 
    # {
    #     'factory': 'LambdaStrFactory',
    #     'lambda_str': 'ev : {low} <= ev.var[0] < {high}',
    #     'name': 'var_cut25',
    #     'low': 25, 'high': 200
    # }

    return ret

##__________________________________________________________________||
def _expand_path_cfg_tuple(path_cfg, alias_dict, overriding_kargs):
    """expand a path config given as a tuple

    Args:
        path_cfg (tuple): a tuple with two elements: (str, dict) 
        alias_dict (dict):
        overriding_kargs (dict):
    """

    # e.g.,
    # path_cfg = ('ev : {low} <= ev.var[0] < {high}', {'low': 10, 'high': 200})
    # overriding_kargs = {'alias': 'var_cut', 'name': 'var_cut25', 'low': 25}

    new_path_cfg = path_cfg[0]
    # e.g., 'ev : {low} <= ev.var[0] < {high}'

    new_overriding_kargs = path_cfg[1].copy()
    # e.g., {'low': 10, 'high': 200}

    new_overriding_kargs.update(overriding_kargs)
    # e.g., {'low': 25, 'high': 200, 'alias': 'var_cut', 'name': 'var_cut25'}

    return expand_path_cfg(
        new_path_cfg,
        overriding_kargs=new_overriding_kargs,
        alias_dict=alias_dict
    )


##__________________________________________________________________||
def _expand_path_cfg_dict(path_cfg, alias_dict):
    if 'factory' in path_cfg:
        return path_cfg

    if not sum([k in path_cfg for k in ('All', 'Any', 'Not')]) <= 1:
        raise ValueError("Any pair of 'All', 'Any', 'Not' cannot be simultaneously given unless factory is given!")

    if 'All' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'AllFactory'
        new_path_cfg['path_cfg_list'] = tuple([expand_path_cfg(p, alias_dict=alias_dict) for p in new_path_cfg.pop('All')])
        return new_path_cfg

    if 'Any' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'AnyFactory'
        new_path_cfg['path_cfg_list'] = tuple([expand_path_cfg(p, alias_dict=alias_dict) for p in new_path_cfg.pop('Any')])
        return new_path_cfg

    if 'Not' in path_cfg:
        new_path_cfg = path_cfg.copy()
        new_path_cfg['factory'] = 'NotFactory'
        new_path_cfg['path_cfg'] = expand_path_cfg(new_path_cfg.pop('Not'), alias_dict=alias_dict)
        return new_path_cfg

    raise ValueError("cannot recognize the path_cfg")

##__________________________________________________________________||
