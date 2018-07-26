# Tai Sakuma <tai.sakuma@gmail.com>
import io
import pytest

from alphatwirl.collector import WriteListToFile

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
    ret = WriteListToFile("tbl.txt")
    ret._open = MockOpen(out)
    ret._close = mockClose
    yield ret

def test_repr(obj):
    repr(obj)

def test_deliver(obj, out):
    results = [
        ('component', 'v1', 'nvar', 'n'),
        ('data1',  100, 6.0,   40),
        ('data1',    2, 9.0, 3.3),
        ('data1', 3124, 3.0, 0.0000001),
        ('data2',  333, 6.0, 300909234),
        ('data2',   11, 2.0, 323432.2234),
    ]

    obj.deliver(results)

    expected = """ component   v1 nvar           n
     data1  100    6          40
     data1    2    9         3.3
     data1 3124    3       1e-07
     data2  333    6   300909234
     data2   11    2 323432.2234
""".encode()

    assert expected == out.getvalue()

def test_deliver_empty_dataframe(obj, out):
    results = [
        ('component', 'v1', 'nvar', 'n'),
    ]

    obj.deliver(results)

    expected = " component v1 nvar n\n".encode()
    assert expected == out.getvalue()

def test_deliver_None_results(obj, out):
    obj.deliver(None)

##__________________________________________________________________||
