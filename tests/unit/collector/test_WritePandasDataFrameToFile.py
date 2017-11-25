import unittest
import io

##__________________________________________________________________||
hasPandas = False
try:
    import pandas
    from alphatwirl.collector import WritePandasDataFrameToFile
    hasPandas = True
except ImportError:
    pass

##__________________________________________________________________||
class MockOpen(object):
    def __init__(self, out):
        self._out = out

    def __call__(self, path):
        return self._out

##__________________________________________________________________||
def mockClose(file): pass

##__________________________________________________________________||
@unittest.skipUnless(hasPandas, "has no pandas")
class TestWritePandasDataFrameToFile(unittest.TestCase):

    @unittest.skip('fail with Pandas 0.20 because of its bug about the header indent')
    def test_deliver(self):
        delivery = WritePandasDataFrameToFile("tbl.txt")

        out = io.BytesIO()
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        results = pandas.DataFrame(
            {
                'v1': [1, 2, 3],
                'n': [4.0, 3.0, 2.0],
                'nvar': [6.0, 9.0, 3.0],
            },
            columns = ['v1', 'n', 'nvar']
            )

        delivery.deliver(results)

        expected = " v1  n  nvar\n  1  4     6\n  2  3     9\n  3  2     3\n".encode()
        self.assertEqual(expected, out.getvalue())

    def test_deliver_empty_dataframe(self):

        delivery = WritePandasDataFrameToFile("tbl.txt")

        out = io.BytesIO()
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        results = pandas.DataFrame(
            {
                'v1': [ ],
                'n': [ ],
                'nvar': [ ],
            },
            columns = ['v1', 'n', 'nvar']
            )

        delivery.deliver(results)

        expected = "v1 n nvar\n".encode()
        self.assertEqual(expected, out.getvalue())

    def test_deliver_None_results(self):

        delivery = WritePandasDataFrameToFile("tbl.txt")

        out = io.BytesIO()
        delivery._open = MockOpen(out)
        delivery._close = mockClose

        delivery.deliver(None)

##__________________________________________________________________||
