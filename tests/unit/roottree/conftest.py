# Tai Sakuma <tai.sakuma@gmail.com>
import sys
import pytest

##__________________________________________________________________||
# @pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")
@pytest.fixture(autouse=True)
def monkeypatch_class_attributes_BranchBuilder(monkeypatch):
    ## monkey patch a class attribute of BranchBuilder.
    ## segmentation violation can happen without this patch.
    ## TODO probably need similar patches for
    ## any other classes with class attributes.
    try:
        module = sys.modules['alphatwirl.roottree.BranchBuilder']
    except KeyError:
        # the exception can happen if ROOT cannot be imported
        yield
        return

    ret =  { }
    monkeypatch.setattr(module.BranchBuilder, 'itsdict', ret)
    yield ret

##__________________________________________________________________||
