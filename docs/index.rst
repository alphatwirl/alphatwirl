.. AlphaTwirl documentation master file, created by
   sphinx-quickstart on Sat May 23 14:38:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AlphaTwirl
=====================

AlphaTwirl is a Python library that contains a set of Python classes which can
be used to loop over event data, summarize them, and store the results for
further analysis or visualization. The input data format that the library
currently supports is ROOT TTrees produced by Heppy, but will be extended to
include the CMS EDM format, e.g., AOD and MiniAOD. An example of summarizing
data is counting events in certain categories. The output format is data frames
in text files, which are convenient for further processes in R or pandas. It can
be also extended to include TTree and Histogram classes in ROOT.


Contents:

.. toctree::
   :maxdepth: 4

   AlphaTwirl


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

