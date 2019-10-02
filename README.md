[![PyPI version](https://badge.fury.io/py/alphatwirl.svg)](https://badge.fury.io/py/alphatwirl) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/alphatwirl/badges/version.svg)](https://anaconda.org/conda-forge/alphatwirl) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597010.svg)](https://doi.org/10.5281/zenodo.597010) [![Build Status](https://travis-ci.org/alphatwirl/alphatwirl.svg?branch=master)](https://travis-ci.org/alphatwirl/alphatwirl) [![codecov](https://codecov.io/gh/alphatwirl/alphatwirl/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/alphatwirl)

<br />

<img src="https://raw.githubusercontent.com/alphatwirl/alphatwirl/v0.11.0/images/AlphaTwirl_logo_black.png" width="500">

---

A Python library for summarizing event data into multivariate categorical data

### Description
_AlphaTwirl_ is a Python library that summarizes event data into multivariate categorical data as data frames. Event data, input to AlphaTwirl, are data with one entry (or row) for one event: for example, data in [ROOT](https://root.cern.ch/) [TTrees](https://root.cern.ch/doc/master/classTTree.html) with one entry per collision event of an [LHC](https://home.cern/topics/large-hadron-collider) experiment at [CERN](http://home.cern/). Event data are often large&mdash;too large to be loaded in memory&mdash;because they have as many entries as events. Multivariate categorical data, the output of AlphaTwirl, have one row for one category. They are usually small&mdash;small enough to be loaded in memory&mdash;because they only have as many rows as categories. Users can, for example, import them as data frames into [R](https://www.r-project.org/) and [pandas](http://pandas.pydata.org/), which usually load all data in memory, and can perform categorical data analyses with a rich set of data operations available in R and pandas.

****

### Quick start

- Jupyter Notebook: [*Quick start of AlphaTwirl*](https://github.com/alphatwirl/notebook-tutorial-2019-02)<br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-tutorial-2019-02/master?filepath=tutorial_01.ipynb)

****

### Publication

- Tai Sakuma, *"AlphaTwirl: A Python library for summarizing event data into multivariate categorical data"*,
  EPJ Web of Conferences **214**, 02001 (2019), [doi:10.1051/epjconf/201921402001](https://doi.org/10.1051/epjconf/201921402001),
  [1905.06609](https://arxiv.org/abs/1905.06609)

****

### License

- AlphaTwirl is licensed under the BSD license.

*****

### Contact

- Tai Sakuma - tai.sakuma@gmail.com
