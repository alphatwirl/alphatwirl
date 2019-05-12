# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.misc import simple_repr

try:
    import cPickle as pickle
except:
    import pickle

##__________________________________________________________________||
@simple_repr
def func():
    return 'called'

def test_simple_repr():
    assert 'called' == func()
    assert 'func' == repr(func)
    assert 'func' == str(func)

def test_pickle():
    p = pickle.dumps(func)
    o = pickle.loads(p)
    assert 'called' == o()

##__________________________________________________________________||
