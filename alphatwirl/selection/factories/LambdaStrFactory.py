# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
def LambdaStrFactory(lambda_str, LambdaStrClass, name = None, **kargs):
    return LambdaStrClass(lambda_str = lambda_str.format(**kargs), name = name)

##__________________________________________________________________||
