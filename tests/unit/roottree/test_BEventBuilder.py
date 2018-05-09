# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

if not has_no_ROOT:
    from alphatwirl.roottree import EventBuilderConfig
    from alphatwirl.roottree import BEventBuilder

##__________________________________________________________________||
pytestmark = pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")

##__________________________________________________________________||
@pytest.fixture()
def obj(request):
    config = EventBuilderConfig(
        inputPaths=['/path/to/input1/tree.root', '/path/to/input2/tree.root'],
        treeName='tree',
        maxEvents=123,
        start=11,
        name='TTJets'
    )
    return BEventBuilder(config)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

##__________________________________________________________________||
