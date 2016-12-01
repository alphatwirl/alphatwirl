#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import os, sys
import errno
import argparse
import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs = argparse.REMAINDER, help = 'paths to task packages')
args = parser.parse_args()

##__________________________________________________________________||
sys.path.insert(1, './bdphi-scripts')
sys.path.insert(1, './bdphi-scripts/bdphiROC')

##__________________________________________________________________||
def main():

    for path in args.paths:

        # e.g., path = 'c/d/task_00003.p'

        taskdir = os.path.dirname(os.path.abspath(path))
        # e.g., '/a/b/c/d'

        result_topdir = os.path.join(taskdir, 'results')
        # e.g., '/a/b/c/d/results'
        mkdir_p(result_topdir)

        f = open(path, 'rb')
        package = pickle.load(f)

        basename = 'task_{:05d}'.format(package.index)
        # e.g., 'task_00003.p'

        resultdir = os.path.join(result_topdir, basename)
        # e.g., '/a/b/c/d/results/task_00003.p'
        mkdir_p(resultdir)

        result = run_task(package.task, package.progressReporter, package.args, package.kwargs)
        result_path = os.path.join(resultdir, 'result.p')
        f = open(result_path, 'wb')
        pickle.dump(result, f)


##__________________________________________________________________||
def run_task(task, progressReporter, args, kwargs):
    try:
        result = task(progressReporter = progressReporter, *args, **kwargs)
    except TypeError:
        result = task(*args, **kwargs)
    return result

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
