
![AlphaTwirl](images/AlphaTwirl.png?raw=true)

---

A Python library for summarizing event data in ROOT Trees

#### Description
The library contains a set of Python classes which can be used to loop over event data, summarize them, and store the results for further analysis or visualization. The input data format that the library currently supports is [ROOT](https://root.cern.ch/) [TTrees](https://root.cern.ch/doc/master/classTTree.html) produced by [Heppy](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHeppy), but will be extended to include the [CMS](http://cms.web.cern.ch/) [EDM](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSSWFramework) format, e.g., [AOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookDataFormats) and [MiniAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD). An example of summarizing data is counting events in certain categories. The output format is data frames in text files, which are convenient for further processes in [R](https://www.r-project.org/) or [pandas](http://pandas.pydata.org/).

