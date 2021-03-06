# Changelog

## [Unreleased]

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.30.0...master))
- cleaned code
- removed the sub-package `progressbar`, replaced with [atpbar](https://github.com/alphatwirl/atpbar)
- updated `.travis.yml`
- reorganized requirements in `requirements` and `setup.py`

## [0.30.0] - 2020-04-11

**PyPI**: https://pypi.org/project/alphatwirl/0.30.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.5...v0.30.0))
- started testing in Python 3.8
- stopped testing in Python 2.7
- updated `README.md`, `.travis.yml`, `setup.py`, unittest

## [0.25.5] - 2019-06-26

**PyPI**: https://pypi.org/project/alphatwirl/0.25.5/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.4...v0.25.5))
- made it possible to override the executable of HTCondor jobs by
  the option `dispatcher_options` of `build_parallel()`
- updated for [\#36](https://github.com/alphatwirl/alphatwirl/issues/36)
    - deprecated `CollectorComposite` and `EventDatasetReader` in `loop`
    - added replacements with the same names in `datasetloop`
- removed the deprecated class `EventsInDatasetReader`
- reorganized modules in `loop`
- updated unittest

## [0.25.4] - 2019-06-17

**PyPI**: https://pypi.org/project/alphatwirl/0.25.4/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.3...v0.25.4))
- deleted deprecated function `listToAlignedText()`
- made minor edits to follow pep 8
- updated unittest

## [0.25.3] - 2019-05-09

**PyPI**: https://pypi.org/project/alphatwirl/0.25.3/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.2...v0.25.3))
- updated `.travis.yml`
    - replaced the channel NLeSC with conda-forge
    - added Python 3.7
    - updated the versions of ROOT and Pandas.
- updated `setup.py`
    - added Python 3.7
- updated docstring in `splitfuncs.py`

## [0.25.2] - 2019-04-11

**PyPI**: https://pypi.org/project/alphatwirl/0.25.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.1...v0.25.2))
- updated `WorkingArea`
    - catch generally `Exception` in `collect_result()` since the job
      needs to be resubmitted regardless of the error type.
    - cleaned code, updated test

## [0.25.1] - 2019-03-30

**PyPI**: https://pypi.org/project/alphatwirl/0.25.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.25.0...v0.25.1))
- cleaned code, docstring, tests for `TaskPackageDropbox`

## [0.25.0] - 2019-03-17

**PyPI**: https://pypi.org/project/alphatwirl/0.25.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.24.2...v0.25.0))
- updated `ResumableDatasetLoop`
    - addressed [\57](https://github.com/alphatwirl/alphatwirl/issues/57)
    - pickle `reader` before having it start reading data as `SubprocessRunner`,
      which is indirectly held by `EventDatasetReader`, becomes unpicklable in
      Python 3
- updated `concurrently`
    - moved `HTCondorJobSubmitter` from `HTCondorJobSubmitter.py` to
      `condor/submitter.py`
    - moved `submit_jobs()`, `query_status_for()`, `change_job_priority()`
      `terminate_jobs()` from `HTCondorJobSubmitter.py` to `condor/commands.py`
    - moved `exec_util.py` to `condor/`
    - `TaskPackage`
        - made it callable
        - moved it to `CommunicationChannel.py`
        - stopped importing it to `concurrently`
    - removed outdated script `example_submit_htcondor.py`
    - updated docstring, tests
    - cleaned code

## [0.24.2] - 2019-03-17

**PyPI**: https://pypi.org/project/alphatwirl/0.24.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.24.1...v0.24.2))
- updated `concurrently`
    - `HTCondorJobSubmitter`:
        - fixed encoding problem in Python 3
        - stop creating the result dir.
        - use `try_executing_until_succeed()` in `run_multiple()`
    - `WorkingArea`:
        - the result dir will be created in `put_package()`
        - renamed `package_path()` `package_relpath()`, deprecating `package_path()`
        - added `package_fullpath()`, `result_relpath()`, `result_fullpath()`
        - changed the default `python_modules` to `None`, avoiding mutable default
    - `try_executing_until_succeed()`
        - added options `input_` and `cwd`
        - updated `logging`
    - updated docstring, tests
    - cleaned code

## [0.24.1] - 2019-03-15

**PyPI**: https://pypi.org/project/alphatwirl/0.24.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.24.0...v0.24.1))
- updated `build_parallel()`
    - removed the deprecated option `htcondor_job_desc_extra`
    - changed default `user_modules` and `dispatcher_options`,
      avoiding mutable default
- updated `HTCondorJobSubmitter`
    - removed the deprecated option `job_desc_extra`
    - changed the default `job_desc_dict` to `None`, avoiding mutable
      default
- updated tests

## [0.24.0] - 2019-03-15

**PyPI**: https://pypi.org/project/alphatwirl/0.24.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.23.3...v0.24.0))
- replaced part of code in `concurrently` with
  [`mantichora`](https://github.com/alphatwirl/mantichora).
- changed how indices are assigned in `CommunicationChannel0` and
  `CommunicationChannel`
    - the index starts from `0` again after `end()` and `begin()` are called
- changed the way to turn off progress bars
    - call `atpbar.disable()`
- updated `README.md`, `setup.py`
- cleaned code

## [0.23.3] - 2019-03-10

**PyPI**: https://pypi.org/project/alphatwirl/0.23.3/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.23.1...v0.23.3))
- added private functions: `_removed_func_option()`,
  `_removed_class_method_option()`
- updated the log message in '_removed()'
- removed
    - a deprecated functions: `build_parallel_multiprocessing()`
- updated required `atpbar` version from 0.9.7 to 1.0.2
- updated `MANIFEST.in`, tests

## [0.23.2] - 2019-02-25

**PyPI**: https://pypi.org/project/alphatwirl/0.23.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.23.1...v0.23.2))
- updated `setup.py`, `.travis.yml`

## [0.23.1] - 2019-02-24

**PyPI**: https://pypi.org/project/alphatwirl/0.23.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.23.0...v0.23.1))
- updated `README.md`, using the full URLs for image files
- used `README.md` as the long description in `setup.py`

## [0.23.0] - 2019-02-24

**PyPI**: https://pypi.org/project/alphatwirl/0.23.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.22.0...v0.23.0))
- promoted the sub-package `progressbar` to an independent package
  [atpbar](https://github.com/alphatwirl/atpbar)
    - added `atpbar` to the default user modules in `parallel`
    - added `atpbar` to `install_requires` in `setup.py`
    - updated `.travis.yml` to install `atpbar`
    - the sub-package `progressbar`, still in `alphatwirl`, is deprecated.

## [0.22.0] - 2019-02-16

**PyPI**: https://pypi.org/project/alphatwirl/0.22.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.21.2...v0.22.0))
- updated progress bars
    - made them properly work for nested loops
    - unnecessitated manual initialization of the progress monitor
        - it starts automatically when the first time atpbar is used
    - removed the progress monitor from `Parallel`
- removed
    - a deprecated object: `EventBuilderConfig`
    - the implementation of deprecated classes: `EventBuilder`,
      `BEventBuilder`
    - an unused class: `EventLoopProgressReportWriter`
    - `build_progressMonitor_communicationChannel()`, the
      implementation of which had been already removed
- updated the log message in '_deprecated()'
- updated requirements for docs (for readthedocs)
- used raw string for regex in `HTCondorJobSubmitter`
- cleaned code

## [0.21.2] - 2019-02-10

**PyPI**: https://pypi.org/project/alphatwirl/0.21.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.21.1...v0.21.2))
- implemented `is_jupyter_notebook()`

## [0.21.1] - 2019-02-10

**PyPI**: https://pypi.org/project/alphatwirl/0.21.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.21.0...v0.21.1))
- removed an unrecognized option (`step`) of `IntProgress`

## [0.21.0] - 2019-02-10

**PyPI**: https://pypi.org/project/alphatwirl/0.21.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.20.3...v0.21.0))
- added progress bars for Jupyter Notebook
- replaced `multiprocessing` with `threading` for progress bars as
  Jupyter Notebook doesn't let a fork to display progress bars
- added function `atpbar`, which initializes `Atpbar`
    - used in `EventLoop` and `ReaderComposite`
- added iterable `Atpbar`, which wraps another iterable and reports
  progress during iterations, inspired by tqdm
- added a link to a quick start tutorial on Jupyter Notebook
  mybinder.org in README.md

## [0.20.3] - 2019-01-25

**PyPI**: https://pypi.org/project/alphatwirl/0.20.3/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.20.2...v0.20.3))
- made the default format for `float` in the output data frame the
  same in python 2 and 3.
- updated the test for pytest 4
- updated the tag line, replacing "multi-dimensional" with "multivariate"
- stopped sleeping needlessly in `TaskPackageDropbox` [\#54](https://github.com/alphatwirl/alphatwirl/pull/54)

## [0.20.2] - 2018-10-12

**PyPI**: https://pypi.org/project/alphatwirl/0.20.2/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.20.1...v0.20.2))
- stopped letting `receive_one()` in `TaskPackageDropbox` unnecessarily
  unpickle all available results, which was needlessly consuming
  memory [\#51](https://github.com/alphatwirl/alphatwirl/pull/51)
- fixed a bug in `_deprecated(msg)`. didn't work correctly when `msg`
  was not given.

## [0.20.1] - 2018-08-15

**PyPI**: https://pypi.org/project/alphatwirl/0.20.1/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.20.0...v0.20.1))
- allowed duplicate dataset names in `EventDatasetReader` [\#50](https://github.com/alphatwirl/alphatwirl/issues/50)

## [0.20.0] - 2018-08-12

**PyPI**: https://pypi.org/project/alphatwirl/0.20.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.19.0...v0.20.0))
- added `collect()` to `AllwCount`, `AnywCount`, `NotwCount`
  [\#33](https://github.com/alphatwirl/alphatwirl/issues/33)
- `mkdir_p()` checks if `path` is empty
- added unittest for `mkdir_p()`
- avoided mutable default of `ReaderComposite`, `AllwCount`,
  `AnywCount`.
- removed the implementation of
  `build_progressMonitor_communicationChannel()`, `atdeprecated()`,
  `atdeprecated_func_option()`, `atdeprecated_class_method_option()`,
  `atrenamed_func_option()`, `atrenamed_class_method_option()`
    - were deprecated
    - now, raise `RuntimeError` if called
- added a decorator `_removed()`
- reimplemented `TableFileNameComposer`
- fixed `ProgressPrint`, avoiding changing dict during iteration

## [0.19.0] - 2018-08-08

**PyPI**: https://pypi.org/project/alphatwirl/0.19.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.8...v0.19.0))
- removed deprecated sub-packages: `cmsedm`, `delphes`, `heppyresult`.
    - the contents of these packages can be found, respectively, in
      the following repositories:
        - https://github.com/alphatwirl/atcmsedm
        - https://github.com/alphatwirl/atdelphes
        - https://github.com/alphatwirl/atheppy

## [0.18.8] - 2018-08-08

**PyPI**: https://pypi.org/project/alphatwirl/0.18.8/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.7...v0.18.8))
- fixed an import error at rtd

## [0.18.7] - 2018-08-07

**PyPI**: https://pypi.org/project/alphatwirl/0.18.7/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.6...v0.18.7))
- changed behavior of `RoundLog`
    - returns the underflow bin for `0` and negative values if `min`
      is given. (previously, returns `0` for `0` and `None` for a
      negative number even when `min` is given)
    - returns the overflow bin for `inf` if `max` is given.
      (previously, returns `None` for `inf` even when `max` is given)
- optimized `RoundLog` and `Round` for speed, e.g., replacing linear
  search with binary search
- updated zenodo badge, using all-versions badge
- organized requirements [\#35](https://github.com/alphatwirl/alphatwirl/issues/35)
    - requirements/doc.txt for sphinx doc, used at Read the Docs
    - requirements/test.txt for test, used at travis-ci
- added CHANGELOG.md

## [0.18.6] - 2018-08-05

**PyPI**: https://pypi.org/project/alphatwirl/0.18.6/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.5...v0.18.6))
- fixed Read The Docs. [\#47](https://github.com/alphatwirl/alphatwirl/issues/40)
- updated README.md
- updated travis-ci config
- updated unittests
