API reference
=============

.. currentmodule:: alphatwirl


binning
-------

.. autosummary::
   :toctree: generated

   binning.Binning
   binning.Echo
   binning.Round
   binning.RoundLog


loop
----
.. autosummary::
   :toctree: generated

   loop.Collector
   loop.CollectorComposite
   loop.CollectorDelegate
   loop.EventLoop
   loop.DatasetIntoEventBuildersSplitter
   loop.EventDatasetReader
   loop.EventLoopProgressReportWriter
   loop.EventLoopRunner
   loop.MPEventLoopRunner
   loop.ReaderComposite
   loop.NullCollector
   loop.ReaderComposite
   loop.splitfuncs.create_files_start_length_list

roottree
--------
.. autosummary::
   :toctree: generated

   roottree.BEventBuilder
   roottree.BEvents
   roottree.Branch
   roottree.EventBuilder
   roottree.Events

selection
---------
.. autosummary::
   :toctree: generated

   selection.build_selection
   selection.modules.All
   selection.modules.Any
   selection.modules.Not
   selection.modules.AllwCount
   selection.modules.AnywCount
   selection.modules.NotwCount
   selection.modules.Count.Count
   selection.modules.LambdaStr.LambdaStr

summary
-------

.. autosummary::
   :toctree: generated

   summary.BackrefMultipleArrayReader
   summary.Count
   summary.KeyValueComposer
   summary.NextKeyComposer
   summary.Reader
   summary.Scan
   summary.Sum
   summary.Summarizer
   summary.WeightCalculatorOne

progressbar
-----------

.. autosummary::
   :toctree: generated

   progressbar.BProgressMonitor
   progressbar.NullProgressMonitor
   progressbar.ProgressBar
   progressbar.ProgressMonitor
   progressbar.ProgressPrint
   progressbar.ProgressReport
   progressbar.ProgressReportPickup
   progressbar.ProgressReporter

concurrently
------------

.. autosummary::
   :toctree: generated

   concurrently.CommunicationChannel
   concurrently.CommunicationChannel0
   concurrently.HTCondorJobSubmitter
   concurrently.MultiprocessingDropbox
   concurrently.SubprocessRunner
   concurrently.TaskPackage
   concurrently.TaskPackageDropbox
   concurrently.Worker
   concurrently.WorkingArea
