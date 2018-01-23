# Tai Sakuma <tai.sakuma@gmail.com>
import os
import stat
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.concurrently import SubprocessRunner

##__________________________________________________________________||
run_py = """
#!/usr/bin/env python
import time
import sys
import os
with open(os.path.join(sys.argv[1], 'sleep.txt'), 'r') as f:
    secs = f.read()
time.sleep(float(secs))
with open(os.path.join(sys.argv[1], 'result.txt'), 'w') as f:
    f.write('{} {} {}'.format(os.getpid(), sys.argv[1], secs))
"""
run_py = run_py.lstrip()

##__________________________________________________________________||
class MockWorkingArea(object):
    def __init__(self, path):
        self.path = path

    def open(self):
        self._prepare_dir(path=self.path)
        self._setup_packages()

    def close(self):
        pass

    def package_path(self, package_index):
        return self.package_path_dict[package_index]

    def _prepare_dir(self, path):
        path_run_py = os.path.join(path, 'run.py')
        with open(path_run_py, 'w') as f:
            f.write(run_py)
        os.chmod(path_run_py, os.stat(path_run_py).st_mode | stat.S_IXUSR)

    def _setup_packages(self):
        os.makedirs(os.path.join(self.path, 'aaa'))
        os.makedirs(os.path.join(self.path, 'bbb'))
        os.makedirs(os.path.join(self.path, 'ccc'))
        with open(os.path.join(self.path, 'aaa', 'sleep.txt'), 'w') as f:
            f.write('0.20')
        with open(os.path.join(self.path, 'bbb', 'sleep.txt'), 'w') as f:
            f.write('0.02')
        with open(os.path.join(self.path, 'ccc', 'sleep.txt'), 'w') as f:
            f.write('0.15')

        self.package_path_dict = {0:'aaa', 1:'bbb', 2:'ccc'}

##__________________________________________________________________||
@pytest.fixture()
def workingarea(tmpdir_factory):
    path = tmpdir_factory.mktemp('')
    path = str(path)
    ret = MockWorkingArea(path=path)
    ret.open()
    yield ret
    ret.close()

def test_MockWorkingArea(workingarea):
    assert 'aaa' == workingarea.package_path(0)
    assert 'bbb' == workingarea.package_path(1)
    assert 'ccc' == workingarea.package_path(2)

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return SubprocessRunner()

def test_repr(obj):
    repr(obj)

def test_run_wait_terminate(obj, workingarea):

    pid1 = obj.run(workingarea, 0)
    pid2 = obj.run(workingarea, 1)
    pid3 = obj.run(workingarea, 2)

    assert {pid1, pid2, pid3} == set(obj.wait())
    # obj.wait() returns a list of finished pids, unsorted

    assert '{} aaa 0.20'.format(pid1) == open(os.path.join(workingarea.path, 'aaa', 'result.txt')).read()
    assert '{} bbb 0.02'.format(pid2) == open(os.path.join(workingarea.path, 'bbb', 'result.txt')).read()
    assert '{} ccc 0.15'.format(pid3) == open(os.path.join(workingarea.path, 'ccc', 'result.txt')).read()

    obj.failed_runids([])

    obj.terminate()

def test_run_poll_terminate():
    # don't explicitly test poll() because the finished jobs are
    # not deterministic. poll() is used by wait() and is
    # indirectly tested through wait().
    pass

def test_run_terminate(obj, workingarea):
    pid1 = obj.run(workingarea, 0)
    pid2 = obj.run(workingarea, 1)
    pid3 = obj.run(workingarea, 2)
    obj.terminate()

def test_wait_terminate(obj):
    assert [ ] == obj.wait()
    obj.terminate()

##__________________________________________________________________||
