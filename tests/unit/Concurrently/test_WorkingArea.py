import unittest
import os
import tempfile
import shutil
import collections
import gzip

try:
   import cPickle as pickle
except:
   import pickle

from AlphaTwirl.Concurrently import WorkingArea
from AlphaTwirl import mkdir_p

##__________________________________________________________________||
MockPackage = collections.namedtuple('MockPackage', 'name')
MockResult = collections.namedtuple('MockResult', 'name')

##__________________________________________________________________||
class TestWorkingArea(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_open(self):
        obj = WorkingArea(dir = self.tmpdir, python_modules = ('AlphaTwirl', ))
        self.assertIsNone(obj.path)
        self.assertIsNone(obj.last_package_index)

        obj.open()
        self.assertIsNotNone(obj.path)
        self.assertEqual(-1, obj.last_package_index)
        self.assertTrue(os.path.isdir(obj.path))
        self.assertTrue(os.path.isfile(os.path.join(obj.path, 'run.py')))
        self.assertTrue(os.path.isfile(os.path.join(obj.path, 'python_modules.tar.gz')))

    def test_put_package(self):
        obj = WorkingArea(dir = self.tmpdir, python_modules = ('AlphaTwirl', ))
        obj.open()

        package1 = MockPackage(name = 'package1')
        package_index, package_path = obj.put_package(package1)
        package_fullpath = os.path.join(obj.path, package_path)
        self.assertTrue(os.path.isfile(package_fullpath))
        f = gzip.open(package_fullpath, 'rb')
        self.assertEqual(package1, pickle.load(f))

    def test_collect_result(self):
        obj = WorkingArea(dir = self.tmpdir, python_modules = ('AlphaTwirl', ))
        obj.open()

        result = MockResult(name = 'result1')

        package_index = 9
        dirname = 'task_{:05d}'.format(package_index)
        result_dir = os.path.join(obj.path, 'results', dirname)
        mkdir_p(result_dir)
        result_path = os.path.join(result_dir, 'result.p.gz')
        f = gzip.open(result_path, 'wb')
        pickle.dump(result, f)
        f.close()

        self.assertEqual(result, obj.collect_result(package_index = package_index))

##__________________________________________________________________||

