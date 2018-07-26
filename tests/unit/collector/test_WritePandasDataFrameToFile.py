# Tai Sakuma <tai.sakuma@gmail.com>
import pytest
import io

##__________________________________________________________________||
has_no_pandas = False
try:
    import pandas as pd
except ImportError:
    has_no_pandas = True

pytestmark = pytest.mark.skipif(has_no_pandas, reason="has no pandas")

if not has_no_pandas:
    from alphatwirl.collector import WritePandasDataFrameToFile

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out):
        self._out = out

    def __call__(self, path):
        return self._out

def mockClose(file):
    pass

##__________________________________________________________________||
@pytest.fixture()
def out():
    return io.BytesIO()

@pytest.fixture()
def obj(out):
    ret = WritePandasDataFrameToFile("tbl.txt")
    ret._open = MockOpen(out)
    ret._close = mockClose
    yield ret

def test_repr(obj):
    repr(obj)

@pytest.mark.xfail(reason='fail with Pandas 0.20 because of its bug about the header indent')
def test_deliver(obj, out):
    results = pd.DataFrame(
        {
            'v1': [1, 2, 3],
            'n': [4.0, 3.0, 2.0],
            'nvar': [6.0, 9.0, 3.0],
        },
        columns = ['v1', 'n', 'nvar']
    )

    obj.deliver(results)

    expected = " v1  n  nvar\n  1  4     6\n  2  3     9\n  3  2     3\n".encode()
    assert expected == out.getvalue()

def test_deliver_empty_dataframe(obj, out):
    results = pd.DataFrame(
        {
            'v1': [ ],
            'n': [ ],
            'nvar': [ ],
        },
        columns = ['v1', 'n', 'nvar']
        )

    obj.deliver(results)

    expected = "v1 n nvar\n".encode()
    assert expected == out.getvalue()

def test_deliver_None_results(obj, out):
    obj.deliver(None)

##__________________________________________________________________||
