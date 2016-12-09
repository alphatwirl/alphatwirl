import unittest
import collections

from AlphaTwirl.Concurrently import TaskPackageDropbox
from AlphaTwirl import mkdir_p

##__________________________________________________________________||
MockPackage = collections.namedtuple('MockPackage', 'idx name path')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class MockWorkingArea(object):
    def __init__(self, path):
        self.path = path
        self.nopened = 0
        self.nclosed = 0
        self.packages = [ ]
        self.results = { }

    def open(self):
        self.nopened += 1

    def close(self):
        self.nclosed += 1

    def put_package(self, package):
        self.packages.append(package)
        return package.idx, package.path

    def collect_result(self, idx):
        return self.results[idx]

##__________________________________________________________________||
class MockDispatcher(object):
    def __init__(self):
        self.runargs = [ ]
        self.nterminated = 0
        self.nwaited = 0

    def run(self, taskdir, package_path):
        self.runargs.append([taskdir, package_path])

    def wait(self):
        self.nwaited += 1

    def terminate(self):
        self.nterminated += 1

##__________________________________________________________________||
class TestTaskPackageDropbox(unittest.TestCase):

    def test_open_close(self):
        workingArea = MockWorkingArea(path = '/A/B')
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea,  dispatcher = dispatcher)

        self.assertEqual(0, workingArea.nopened)
        self.assertEqual(0, workingArea.nclosed)
        self.assertEqual(0, dispatcher.nterminated)

        obj.open()
        self.assertEqual(1, workingArea.nopened)
        self.assertEqual(0, workingArea.nclosed)
        self.assertEqual(0, dispatcher.nterminated)

        obj.close()
        self.assertEqual(1, workingArea.nopened)
        self.assertEqual(1, workingArea.nclosed)
        self.assertEqual(1, dispatcher.nterminated)

    def test_open_put_receive_close(self):
        workingArea = MockWorkingArea(path = '/A/B')
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea,  dispatcher = dispatcher)

        #
        # open
        #
        obj.open()

        #
        # put
        #
        package0 = MockPackage(idx = 0, name = 'package0', path = 'c/d/0')
        obj.put(package0)

        package1 = MockPackage(idx = 1, name = 'package1', path = 'c/d/1')
        obj.put(package1)

        self.assertEqual([package0, package1], workingArea.packages)
        self.assertEqual(2, len(dispatcher.runargs))
        self.assertEqual(['/A/B', 'c/d/0'], dispatcher.runargs[0])
        self.assertEqual(['/A/B', 'c/d/1'], dispatcher.runargs[1])

        #
        # receive
        #
        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        workingArea.results.update({0: result0, 1: result1})
        self.assertEqual(0, dispatcher.nwaited)
        self.assertEqual([result0, result1], obj.receive())
        self.assertEqual(1, dispatcher.nwaited)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

##__________________________________________________________________||
