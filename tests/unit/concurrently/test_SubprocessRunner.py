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
run_py_content = """
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
run_py_content = run_py_content.lstrip()

##__________________________________________________________________||
@pytest.fixture()
def taskdir(tmpdir_factory):
    ret = tmpdir_factory.mktemp('')
    ret = str(ret)
    path_run_py = os.path.join(ret, 'run.py')
    with open(path_run_py, 'w') as f:
        f.write(run_py_content)
        os.chmod(path_run_py, os.stat(path_run_py).st_mode | stat.S_IXUSR)
    return ret

@pytest.fixture()
def package0(taskdir):
    os.makedirs(os.path.join(taskdir, 'aaa'))
    with open(os.path.join(taskdir, 'aaa', 'sleep.txt'), 'w') as f:
            f.write('0.20')

@pytest.fixture()
def package1(taskdir):
    os.makedirs(os.path.join(taskdir, 'bbb'))
    with open(os.path.join(taskdir, 'bbb', 'sleep.txt'), 'w') as f:
            f.write('0.02')

@pytest.fixture()
def package2(taskdir):
    os.makedirs(os.path.join(taskdir, 'ccc'))
    with open(os.path.join(taskdir, 'ccc', 'sleep.txt'), 'w') as f:
            f.write('0.15')

@pytest.fixture()
def workingarea(taskdir, package0, package1, package2):
    ret = mock.MagicMock(path=taskdir)
    package_path_dict = {0:'aaa', 1:'bbb', 2:'ccc'}
    ret.package_path.side_effect = lambda x: package_path_dict[x]
    return ret

def test_MockWorkingArea(workingarea):
    assert 'aaa' == workingarea.package_path(0)
    assert 'bbb' == workingarea.package_path(1)
    assert 'ccc' == workingarea.package_path(2)

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return SubprocessRunner()

##__________________________________________________________________||
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
    # don't explicitly test poll() because the finished tasks are not
    # deterministic. poll() is used by wait() and is indirectly tested
    # through wait().
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
