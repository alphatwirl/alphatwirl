# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

from alphatwirl.heppyresult import EventBuilderConfig

if not has_no_ROOT:
    from alphatwirl.heppyresult import EventBuilderConfigMaker

##__________________________________________________________________||
@pytest.fixture()
def analyzer():
    return mock.Mock(path = '/heppyresult/dir/TTJets/treeProducerSusyAlphaT')

@pytest.fixture()
def component(analyzer):
    ret = mock.Mock(treeProducerSusyAlphaT=analyzer)
    ret.configure_mock(name='TTJets')
    return ret

##__________________________________________________________________||
def test_repr():
    obj = EventBuilderConfigMaker(
        analyzerName='treeProducerSusyAlphaT',
        fileName='tree.root',
        treeName='tree'
    )
    print obj

@pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")
def test_create_config_for(component):
    obj = EventBuilderConfigMaker(
        analyzerName='treeProducerSusyAlphaT',
        fileName='tree.root',
        treeName='tree'
    )

    expected = EventBuilderConfig(
        inputPaths=['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root'],
        treeName='tree',
        maxEvents=30,
        start=20,
        name='TTJets',
        component = component,
    )


    actual = obj.create_config_for(
        component,
        files=['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root'],
        start=20,
        length=30
    )

    assert expected == actual

def test_file_list_in(component):
    obj = EventBuilderConfigMaker(
        analyzerName='treeProducerSusyAlphaT',
        fileName='tree.root',
        treeName='tree'
    )

    expected = ['/heppyresult/dir/TTJets/treeProducerSusyAlphaT/tree.root']

    actual = obj.file_list_in(component)

    assert expected == actual

def test_file_list_in_maxFiles(component):
    obj = EventBuilderConfigMaker(
        analyzerName='treeProducerSusyAlphaT',
        fileName='tree.root',
        treeName='tree'
    )

    expected = [ ]

    actual = obj.file_list_in(component, maxFiles=0)

    assert expected == actual

##__________________________________________________________________||
