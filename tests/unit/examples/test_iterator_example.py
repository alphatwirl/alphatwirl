import alphatwirl
import unittest

##__________________________________________________________________||
def genFunc():
    yield 101
    yield 102
    yield 103

##__________________________________________________________________||
class IteClass(object):
    def __init__(self):
        self.val = 100
        pass

    def __iter__(self):
        self.val = 101
        yield self
        self.val = 102
        yield self
        self.val = 103
        yield self

##__________________________________________________________________||
class TestExampleGeneratorFunction(unittest.TestCase):

    def test_genFunc_Iteration(self):
        self.assertEqual([101, 102, 103], [e for e in genFunc()])

    def test_genFunc_ManualIteration(self):
        gen = genFunc()
        it = iter(gen)
        self.assertIs(it, gen)
        self.assertEqual(101, next(it))
        self.assertEqual(102, next(it))
        self.assertEqual(103, next(it))
        self.assertRaises(StopIteration, next, it)

##__________________________________________________________________||
class TestExampleIterableObject(unittest.TestCase):

    def test_iteObj_Iteration(self):
        self.assertEqual([101, 102, 103], [i.val for i in IteClass()])

    def test_iteObj_ManualIteration(self):
        itObj = IteClass()
        self.assertEqual(100, itObj.val)
        it = iter(itObj)
        itObj1 = next(it)
        self.assertIs(itObj, itObj1)
        self.assertEqual(101, itObj1.val)
        itObj2 = next(it)
        self.assertIs(itObj, itObj2)
        self.assertEqual(102, itObj2.val)
        itObj3 = next(it)
        self.assertIs(itObj, itObj3)
        self.assertEqual(103, itObj3.val)
        self.assertRaises(StopIteration, next, it)


##__________________________________________________________________||
