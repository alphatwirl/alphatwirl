import unittest
import logging
import collections

from alphatwirl.concurrently import TaskPackageDropbox
from alphatwirl import mkdir_p

##__________________________________________________________________||
MockPackage = collections.namedtuple('MockPackage', 'idx name path')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class MockWorkingArea(object):
    def __init__(self):
        self.nopened = 0
        self.nclosed = 0
        self.packages = [ ]
        self.results = collections.defaultdict(collections.deque)
        self.package_path_dict = { }

    def open(self):
        self.nopened += 1

    def close(self):
        self.nclosed += 1

    def put_package(self, package):
        self.packages.append(package)
        self.package_path_dict[package.idx] = package.path
        return package.idx

    def package_path(self, package_index):
        return self.package_path_dict[package_index]

    def collect_result(self, idx):
        return self.results[idx].popleft()

##__________________________________________________________________||
class MockDispatcher(object):
    def __init__(self):
        self.runargs = [ ]
        self.nterminated = 0
        self.npolled = 0
        self.run_returns = collections.deque()
        self.poll_returns = collections.deque()
        self.failed_runids_args = [ ]

    def run(self, workingArea, package_index):
        self.runargs.append([workingArea, package_index])
        return self.run_returns.popleft()

    def poll(self):
        self.npolled += 1
        return self.poll_returns.popleft()

    def failed_runids(self, runids):
        self.failed_runids_args.append(runids)

    def terminate(self):
        self.nterminated += 1

##__________________________________________________________________||
class TestTaskPackageDropbox(unittest.TestCase):

    def test_repr(self):
        workingArea = MockWorkingArea()
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea, dispatcher = dispatcher, sleep = 0.01)
        repr(obj)

    def test_open_close(self):
        workingArea = MockWorkingArea()
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea, dispatcher = dispatcher, sleep = 0.01)

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
        workingArea = MockWorkingArea()
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea, dispatcher = dispatcher, sleep = 0.01)

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
        self.assertEqual([workingArea, 0], dispatcher.runargs[0])
        self.assertEqual([workingArea, 1], dispatcher.runargs[1])

        #
        # receive
        #
        dispatcher.poll_returns.extend([[1001, 1002]])

        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        workingArea.results[0].extend([result0])
        workingArea.results[1].extend([result1])
        self.assertEqual(0, dispatcher.npolled)
        self.assertEqual([result0, result1], obj.receive())
        self.assertEqual(1, dispatcher.npolled)
        self.assertEqual([[ ]], dispatcher.failed_runids_args)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

    def test_finished_in_steps(self):
        workingArea = MockWorkingArea()
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea, dispatcher = dispatcher, sleep = 0.01)

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
        self.assertEqual([workingArea, 0], dispatcher.runargs[0])
        self.assertEqual([workingArea, 1], dispatcher.runargs[1])
        self.assertEqual([workingArea, 2], dispatcher.runargs[2])

        #
        # receive
        #
        dispatcher.poll_returns.extend([[1001, 1003], [ ], [1002]])

        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        result2 = MockResult(name = 'result2')
        workingArea.results[0].extend([result0])
        workingArea.results[1].extend([result1])
        workingArea.results[2].extend([result2])
        self.assertEqual(0, dispatcher.npolled)
        self.assertEqual([result0, result1, result2], obj.receive())
        self.assertEqual(3, dispatcher.npolled)
        self.assertEqual([[ ], [ ], [ ]], dispatcher.failed_runids_args)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

    def test_rerun(self):
        workingArea = MockWorkingArea()
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(workingArea = workingArea, dispatcher = dispatcher, sleep = 0.01)

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
        self.assertEqual([workingArea, 0], dispatcher.runargs[0])
        self.assertEqual([workingArea, 1], dispatcher.runargs[1])
        self.assertEqual([workingArea, 2], dispatcher.runargs[2])

        #
        # receive
        #
        dispatcher.poll_returns.extend([[1001, 1003], [ ], [1002, 1004], [1005]])
        dispatcher.run_returns.extend([1004, 1005])

        result0 = MockResult(name = 'result0')
        result1 = MockResult(name = 'result1')
        result2 = MockResult(name = 'result2')
        workingArea.results[0].extend([result0])
        workingArea.results[1].extend([result1])
        workingArea.results[2].extend([None, None, result2]) # fail twice before success
        self.assertEqual(0, dispatcher.npolled)

        ## logging.getLogger('alphatwirl').setLevel(logging.DEBUG)

        self.assertEqual([result0, result1, result2], obj.receive())

        self.assertEqual(4, dispatcher.npolled)

        self.assertEqual([[1003], [ ], [1004], [ ]], dispatcher.failed_runids_args)

        #
        # close
        #
        self.assertEqual(0, dispatcher.nterminated)
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

##__________________________________________________________________||
