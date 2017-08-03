[![Build Status](https://travis-ci.org/alphatwirl/alphatwirl.svg?branch=v0.9.x)](https://travis-ci.org/alphatwirl/alphatwirl) [![DOI](https://zenodo.org/badge/30841569.svg)](https://zenodo.org/badge/latestdoi/30841569)


[<img src="images/AlphaTwirl.png" width="500">](images/AlphaTwirl.png?raw=true)

---

A python library for summarizing event data into multi-dimensional categorical data

#### Description
The library contains a set of Python classes which can be used to loop over event data, summarize them, and store the results for further analysis or visualization. Event data here are defined as any data with one row (or entry) for one event; for example, data in [ROOT](https://root.cern.ch/) [TTrees](https://root.cern.ch/doc/master/classTTree.html) are event data when they have one entry for one proton-proton collision event. Outputs of this library are typically not event data but multi-dimensional categorical data, which have one row for one category. Therefore, the outputs can be imported into [R](https://www.r-project.org/) or [pandas](http://pandas.pydata.org/) as data frames. Then, users can continue a multi-dimensional categorical analysis with R, pandas, and other modern data analysis tools.
