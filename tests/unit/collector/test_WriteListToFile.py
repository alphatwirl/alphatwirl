import unittest
# import cStringIO
import io

from alphatwirl.collector import WriteListToFile

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out): self._out = out
    def __call__(self, path): return self._out

##__________________________________________________________________||
def mockClose(file): pass

##__________________________________________________________________||
class TestWriteListToFile(unittest.TestCase):

    def test_repr(self):
        obj = WriteListToFile("tbl.txt")
        repr(obj)

    def test_deliver(self):
        delivery = WriteListToFile("tbl.txt")

        out = io.BytesIO()
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        results = [
            ('component', 'v1', 'nvar', 'n'),
            ('data1',  100, 6.0,   40),
            ('data1',    2, 9.0, 3.3),
            ('data1', 3124, 3.0, 0.0000001),
            ('data2',  333, 6.0, 300909234),
            ('data2',   11, 2.0, 323432.2234),
        ]

        delivery.deliver(results)

        expected = """ component   v1 nvar           n
     data1  100    6          40
     data1    2    9         3.3
     data1 3124    3       1e-07
     data2  333    6   300909234
     data2   11    2 323432.2234
""".encode()

        self.assertEqual(expected, out.getvalue())

    def test_deliver_empty_dataframe(self):

        delivery = WriteListToFile("tbl.txt")

        out = io.BytesIO()
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        results = [
            ('component', 'v1', 'nvar', 'n'),
        ]

        delivery.deliver(results)

        expected = " component v1 nvar n\n".encode()
        self.assertEqual(expected, out.getvalue())

    def test_deliver_None_results(self):

        delivery = WriteListToFile("tbl.txt")

        out = io.BytesIO
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        delivery.deliver(None)

##__________________________________________________________________||
