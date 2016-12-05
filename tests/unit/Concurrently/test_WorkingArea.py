import unittest
import os
import tempfile
import shutil
import collections
import pickle

from AlphaTwirl.Concurrently import WorkingArea
from AlphaTwirl.mkdir_p import mkdir_p

##__________________________________________________________________||
MockPackage = collections.namedtuple('MockPackage', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class TestWorkingArea(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_init(self):
        obj = WorkingArea(dir = self.tmpdir)
        self.assertTrue(os.path.isdir(obj.path))
        self.assertTrue(os.path.isfile(os.path.join(obj.path, 'run.py')))

    def test_put_python_modules(self):
        obj = WorkingArea(dir = self.tmpdir)
        obj.put_python_modules(modules = ('AlphaTwirl', ))
        self.assertTrue(os.path.isfile(os.path.join(obj.path, 'python_modules.tar.gz')))

    def test_put_package(self):
        obj = WorkingArea(dir = self.tmpdir)

        package1 = MockPackage(name = 'package1')
        package_index, package_path = obj.put_package(package1)
        package_fullpath = os.path.join(obj.path, package_path)
        self.assertTrue(os.path.isfile(package_fullpath))
        f = open(package_fullpath, 'rb')
        self.assertEqual(package1, pickle.load(f))

    def test_collect_result(self):
        obj = WorkingArea(dir = self.tmpdir)

        result = MockResult(name = 'result1')

        package_index = 9
        dirname = 'task_{:05d}'.format(package_index)
        result_dir = os.path.join(obj.path, 'results', dirname)
        mkdir_p(result_dir)
        result_path = os.path.join(result_dir, 'result.p')
        f = open(result_path, 'wb')
        pickle.dump(result, f)
        f.close()

        self.assertEqual(result, obj.collect_result(package_index = package_index))

##__________________________________________________________________||

