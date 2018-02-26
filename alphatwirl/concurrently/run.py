#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function

import os, sys
import errno
import argparse
import tarfile
import signal
import gzip
import json
import logging
import cProfile, pstats

from io import StringIO, BytesIO

try:
    import cPickle as pickle
except:
    import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs=argparse.REMAINDER, help='paths to task packages')
parser.add_argument('--profile', action='store_true', help='run profile')
parser.add_argument('--profile-out-path', default=None, help='path to write the result of profile')
args = parser.parse_args()

##__________________________________________________________________||
signal.signal(signal.SIGINT, signal.SIG_IGN)

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
    print('\n'.join(messages), file=sys.stderr)

##__________________________________________________________________||
def setup():
    setup_logging()
    setup_python_modules()

def setup_logging():
    path = 'logging_levels.json.gz'
    if not os.path.isfile(path):
        return
    with gzip.GzipFile(path, 'r') as f:
        loglevel_dict = json.loads(f.read().decode('utf-8'))

    for name, level in loglevel_dict.items():
        logger = logging.getLogger(name)
        logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)


def setup_python_modules():

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
    with gzip.open(result_path, 'wb') as f:
        pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)

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
def print_profile_func(func, profile_out_path=None):
    result = profile_func(func)
    if profile_out_path is None:
        print(result)
    else:
        with open(profile_out_path, 'w') as f:
            f.write(result)

##__________________________________________________________________||
def profile_func(func):
    pr = cProfile.Profile()
    pr.enable()
    func()
    pr.disable()
    sortby = 'cumulative'
    try:
        s = StringIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    except TypeError:
        s = BytesIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    return s.getvalue()

##__________________________________________________________________||
if __name__ == '__main__':
    if args.profile:
        print_profile_func(
            func=main,
            profile_out_path=args.profile_out_path
        )
    else:
        main()

##__________________________________________________________________||
