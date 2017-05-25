#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
from __future__ import print_function

import os, sys
import errno
import argparse
import tarfile
import gzip

try:
    import cPickle as pickle
except:
    import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs = argparse.REMAINDER, help = 'paths to task packages')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    try:
        run_tasks()
    except Exception as e:
        print_logs(e)
        raise

##__________________________________________________________________||
def run_tasks():

    setup()

    for package_path in args.paths:

        # e.g., package_path = 'task_00003.p.gz',
        # a relative to the directory in which this file is stored

        thisdir = os.path.dirname(__file__)
        package_path = os.path.join(thisdir, package_path)
        # e.g., package_path = 'c/d/task_00003.p.gz'

        result = run(package_path)

        result_path = compose_result_path(package_path)
        # e.g., '/a/b/c/d/results/task_00003/result.p.gz'

        store_result(result, result_path)

##__________________________________________________________________||
def print_logs(error):
    import socket
    import datetime
    messages = [
        '',
        '{:>20}: {}'.format('error', error),
        '{:>20}: {}'.format('sys.argv', sys.argv),
        '{:>20}: {}'.format('time', datetime.datetime.now()),
        '{:>20}: {}'.format('hostname', socket.getfqdn()),
        '{:>20}: {}'.format('pwd', os.getcwd()),
        '{:>20}: {}'.format('ls', ', '.join(sorted(os.listdir(os.getcwd())))),
        '{:>20}: {}'.format('sys.path', ', '.join(sys.path)),
        '{:>20}: {}'.format('os.environ', os.environ)

    ]
    print('\n'.join(messages), file = sys.stderr)

##__________________________________________________________________||
def setup():
    dirname = 'python_modules'
    tarname = dirname + '.tar.gz'

    if os.path.exists(tarname) and not os.path.exists(dirname):
        if try_make_file('.untarring'):
            tar = tarfile.open(tarname)
            tar.extractall()
            tar.close()
            os.remove('.untarring')

    while os.path.isfile('.untarring'):
       pass

    if not os.path.exists(dirname): return

    sys.path.insert(0, dirname)

##_______________________________________________________________||
# http://stackoverflow.com/questions/33223564/atomically-creating-a-file-if-it-doesnt-exist-in-python
def try_make_file(filename):
    try:
        os.open(filename,  os.O_CREAT | os.O_EXCL)
        return True
    except OSError:
        # FileExistsError can be used for Python 3
        return False

##__________________________________________________________________||
def run(package_path):
    f = gzip.open(package_path, 'rb')
    package = pickle.load(f)
    result = package.task(*package.args, **package.kwargs)
    return result

##__________________________________________________________________||
def compose_result_path(package_path):

    # e.g., package_path = 'c/d/task_00003.p.gz'

    taskdir = os.path.dirname(os.path.abspath(package_path))
    # e.g., '/a/b/c/d'

    result_topdir = os.path.join(taskdir, 'results')
    # e.g., '/a/b/c/d/results'

    package_basename =  os.path.basename(package_path)
    # e.g., 'task_00003.p.gz'

    resultdir_basename = os.path.splitext(package_basename)[0]
    resultdir_basename = os.path.splitext(resultdir_basename)[0]
    # e.g., 'task_00003'

    resultdir = os.path.join(result_topdir, resultdir_basename)
    # e.g., '/a/b/c/d/results/task_00003'

    result_path = os.path.join(resultdir, 'result.p.gz')
    # e.g., '/a/b/c/d/results/task_00003/result.p.gz'

    return result_path

##__________________________________________________________________||
def store_result(result, result_path):
    mkdir_p(os.path.dirname(result_path))
    f = gzip.open(result_path, 'wb')
    pickle.dump(result, f, protocol = pickle.HIGHEST_PROTOCOL)

##__________________________________________________________________||
def mkdir_p(path):
    # http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

##__________________________________________________________________||
if __name__ == '__main__':
    main()
