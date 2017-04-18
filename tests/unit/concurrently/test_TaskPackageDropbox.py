import unittest
import collections

from alphatwirl.concurrently import TaskPackageDropbox
from alphatwirl import mkdir_p

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
        self.npolled = 0
        self.runids = collections.deque()
        self.last_runid = 32349
        self.nfinished = 0
        self.run_returns = collections.deque()
        self.poll_returns = collections.deque()

    def run(self, taskdir, package_path):
        self.runargs.append([taskdir, package_path])
        self.last_runid += 1
        self.runids.append(self.last_runid)
        return self.run_returns.popleft()

    def poll(self):
        self.npolled += 1
        return self.poll_returns.popleft()

    def terminate(self):
        self.nterminated += 1

##__________________________________________________________________||
class TestTaskPackageDropbox(unittest.TestCase):

    def test_repr(self):
        workingArea = MockWorkingArea(path = '/A/B')
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea,  dispatcher = dispatcher)
        repr(obj)

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

    def test_all_finished_once(self):
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
        dispatcher.run_returns.extend([1001, 1002])

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
        dispatcher.poll_returns.extend([[1001, 1002]])

        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        workingArea.results.update({0: result0, 1: result1})
        self.assertEqual(0, dispatcher.npolled)
        self.assertEqual([result0, result1], obj.receive())
        self.assertEqual(1, dispatcher.npolled)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

    def test_finished_in_steps(self):
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
        dispatcher.run_returns.extend([1001, 1002, 1003])

        package0 = MockPackage(idx = 0, name = 'package0', path = 'c/d/0')
        obj.put(package0)

        package1 = MockPackage(idx = 1, name = 'package1', path = 'c/d/1')
        obj.put(package1)

        package2 = MockPackage(idx = 2, name = 'package2', path = 'c/d/2')
        obj.put(package2)

        self.assertEqual([package0, package1, package2], workingArea.packages)
        self.assertEqual(3, len(dispatcher.runargs))
        self.assertEqual(['/A/B', 'c/d/0'], dispatcher.runargs[0])
        self.assertEqual(['/A/B', 'c/d/1'], dispatcher.runargs[1])
        self.assertEqual(['/A/B', 'c/d/2'], dispatcher.runargs[2])

        #
        # receive
        #
        dispatcher.poll_returns.extend([[1001, 1003], [ ], [1002]])

        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        result2 = MockResult(name = 'result2')
        workingArea.results.update({0: result0, 1: result1, 2: result2})
        self.assertEqual(0, dispatcher.npolled)
        self.assertEqual([result0, result1, result2], obj.receive())
        self.assertEqual(3, dispatcher.npolled)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

##__________________________________________________________________||
