#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import os, sys
import glob
import argparse
import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('taskdir', help = 'path to a dir with task packages')
args = parser.parse_args()

##__________________________________________________________________||
sys.path.insert(1, './bdphi-scripts')
sys.path.insert(1, './bdphi-scripts/bdphiROC')

##__________________________________________________________________||
def run_task(task, progressReporter, args, kwargs):
    try:
        result = task(progressReporter = progressReporter, *args, **kwargs)
    except TypeError:
        result = task(*args, **kwargs)
    return result

##__________________________________________________________________||
pattern = os.path.join(args.taskdir, 'task_*.p')
# e.g., '_ccsp_temp/ccsp_20161129_131104_mBcOmO/task_*.p'

package_paths = sorted(glob.glob(pattern))

result_topdir = os.path.join(args.taskdir, 'results')
os.mkdir(result_topdir)

for path in package_paths:
    f = open(path, 'rb')
    package = pickle.load(f)
    basename = 'task_{:05d}'.format(package.index)
    resultdir = os.path.join(result_topdir, basename)
    os.mkdir(resultdir)
    result = run_task(package.task, package.progressReporter, package.args, package.kwargs)
    result_path = os.path.join(resultdir, 'result.p')
    f = open(result_path, 'wb')
    pickle.dump(result, f)

##__________________________________________________________________||
