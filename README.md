
![AlphaTwirl](images/AlphaTwirl.png?raw=true)

---

A Python library for summarizing event data in CMS EDM and Heppy flat trees

#### Description
The library contains a set of Python classes which can be used to loop over event data, summarize them, and store the results for further analysis or visualization. The input data format that the library currently supports is ROOT TTrees produced by Heppy, but will be extended to include the CMS EDM format, e.g., AOD and MiniAOD. An example of summarizing data is counting events in certain categories. The output format is data frames in text files, which are convenient for further processes in R or pandas. It can be also extended to include TTree and Histogram classes in ROOT.

#### Features
 * a tree entry as a Python iterator
 * aware of the directory structure of Heppy results
 * well refactored, e.g., the input formats, the summarizing methods, the output formats are decoupled.
 * clean-code, unit test in place, which facilitate the rapid development of new functionalities, i.e, you will know when an existing functionality breaks. There won't be an extended period of debugging in the end.
 * multiprocessing - all cores in your computer can be simultaneously used
 * progress bars - you will know how long you need to wait
