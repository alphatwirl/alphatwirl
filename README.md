[![PyPI version](https://badge.fury.io/py/alphatwirl.svg)](https://badge.fury.io/py/alphatwirl) [![DOI](https://zenodo.org/badge/30841569.svg)](https://zenodo.org/badge/latestdoi/30841569) [![Build Status](https://travis-ci.org/alphatwirl/alphatwirl.svg?branch=v0.9.x)](https://travis-ci.org/alphatwirl/alphatwirl) [![codecov](https://codecov.io/gh/alphatwirl/alphatwirl/branch/v0.9.x/graph/badge.svg)](https://codecov.io/gh/alphatwirl/alphatwirl)


[<img src="images/AlphaTwirl.png" width="500">](images/AlphaTwirl.png?raw=true)

---

A python library for summarizing event data into multi-dimensional categorical data

#### Description
_alphatwirl_ is a python library that loops over event data and summarizes them into multi-dimensional categorical data for further analysis and visualization. Event data are any data with one row (or entry) for one event: for example, data in [ROOT](https://root.cern.ch/) [TTrees](https://root.cern.ch/doc/master/classTTree.html) when they have one entry for one collision event of a collider experiment such as the [LHC](https://home.cern/topics/large-hadron-collider) at [CERN](http://home.cern/). Multi-dimensional categorical data have one row for one category: they can be represented by data frames. After summarizing event data into multi-dimensional categorical data as data frames, users can, for example, import the data frames into [R](https://www.r-project.org/) or [pandas](http://pandas.pydata.org/) and continue the analysis and visualization in R or pandas.
