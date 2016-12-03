import unittest
import os
import tempfile
import shutil
import collections
import pickle

from AlphaTwirl.ConcurrentlySP import TaskPackageDropbox
from AlphaTwirl.mkdir_p import mkdir_p

##__________________________________________________________________||
MockPackage = collections.namedtuple('MockPackage', 'name')
MockResult = collections.namedtuple('MockResult', 'package')

##__________________________________________________________________||
class MockDispatcher(object):
    def __init__(self):
        self.runargs = [ ]
        self.nterminated = 0

    def run(self, taskdir, package_path):
        self.runargs.append([taskdir, package_path])

    def wait(self):
        for taskdir, package_path in self.runargs:

            # retrieve package
            f = open(os.path.join(taskdir, package_path), 'rb')
            package = pickle.load(f)

            # create result
            result = MockResult(package = package)

            # store result
            resultdir = os.path.join(taskdir, 'results', os.path.splitext(package_path)[0])
            resultpath = os.path.join(resultdir, 'result.p')
            mkdir_p(os.path.dirname(resultpath))
            f = open(resultpath, 'wb')
            pickle.dump(result, f)

        self.runargs[:] = [ ]

    def terminate(self):
        self.nterminated += 1

##__________________________________________________________________||
class TestTaskPackageDropbox(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_open_close(self):
        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(dispatcher = dispatcher, path = self.tmpdir)

        obj.open()
        self.assertEqual(0, dispatcher.nterminated)

        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

    def test_open_put_receive_close(self):

        dispatcher = MockDispatcher()
        obj = TaskPackageDropbox(dispatcher = dispatcher, path = self.tmpdir)

        #
        # open
        #
        obj.open()

        #
        # put
        #
        package1 = MockPackage('package1')
        obj.put(package1)

        package2 = MockPackage('package2')
        obj.put(package2)

        self.assertEqual(2, len(dispatcher.runargs))

        # package1
        taskdir, package_path = dispatcher.runargs[0]
        self.assertEqual(self.tmpdir, os.path.dirname(taskdir))
        self.assertTrue(os.path.isfile(os.path.join(taskdir, 'run.py')))
        package_fullpath = os.path.join(taskdir, package_path)
        self.assertTrue(os.path.isfile(package_fullpath))
        f = open(package_fullpath, 'rb')
        self.assertEqual(package1, pickle.load(f))

        # package2
        taskdir, package_path = dispatcher.runargs[1]
        self.assertEqual(self.tmpdir, os.path.dirname(taskdir))
        self.assertTrue(os.path.isfile(os.path.join(taskdir, 'run.py')))
        package_fullpath = os.path.join(taskdir, package_path)
        self.assertTrue(os.path.isfile(package_fullpath))
        f = open(package_fullpath, 'rb')
        self.assertEqual(package2, pickle.load(f))

        #
        # receive
        #
        expected = [MockResult(package1), MockResult(package2)]
        self.assertEqual(expected, obj.receive())

        #
        # close
        #
        obj.close()
        self.assertEqual(1, dispatcher.nterminated)

##__________________________________________________________________||

