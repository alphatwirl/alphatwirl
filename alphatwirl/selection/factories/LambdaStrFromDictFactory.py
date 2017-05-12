# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def LambdaStrFromDictFactory(key, **kargs):
    return kargs['LambdaStrClass'](lambda_str = kargs['aliasDict'][key].format(**kargs), name = key)

##__________________________________________________________________||
