import unittest
import inspect

import alphatwirl

##__________________________________________________________________||
hasPandas = False
try:
    import pandas
    hasPandas = True
except ImportError:
    pass


##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

##__________________________________________________________________||

class TestImport_01(unittest.TestCase):

    @unittest.skipUnless(hasPandas, "has no pandas")
    def test_with_pandas(self):
        self.assertTrue(inspect.isclass(alphatwirl.collector.ToDataFrameWithDatasetColumn))
        self.assertTrue(inspect.isclass(alphatwirl.collector.WritePandasDataFrameToFile))

    @unittest.skipUnless(hasROOT, "has no ROOT")
    def test_with_ROOT(self):
        self.assertTrue(inspect.isclass(alphatwirl.roottree.BEvents))
        self.assertTrue(inspect.isclass(alphatwirl.roottree.BranchAddressManagerForVector))

        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.EventBuilder))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.EventBuilderConfigMaker))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblBranch))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblTree))

    def test_functions(self):
        self.assertTrue(inspect.isfunction(alphatwirl.mkdir_p))

        self.assertTrue(inspect.isfunction(alphatwirl.configure.build_counter_collector_pair))
        self.assertTrue(inspect.isfunction(alphatwirl.configure.build_progressMonitor_communicationChannel))

    def test_classes(self):
        self.assertTrue(inspect.isclass(alphatwirl.binning.Binning))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Echo))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Round))
        self.assertTrue(inspect.isclass(alphatwirl.binning.RoundLog))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Combine))
        self.assertTrue(inspect.isclass(alphatwirl.collector.ToTupleListWithDatasetColumn))
        self.assertTrue(inspect.isclass(alphatwirl.collector.WriteListToFile))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.CommunicationChannel))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.CommunicationChannel0))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.TaskPackage))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.TaskPackageDropbox))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.MultiprocessingDropbox))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.SubprocessRunner))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.WorkingArea))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.HTCondorJobSubmitter))
        self.assertTrue(inspect.isclass(alphatwirl.configure.TableConfigCompleter))
        self.assertTrue(inspect.isclass(alphatwirl.configure.TableFileNameComposer))
        self.assertTrue(inspect.isclass(alphatwirl.roottree.Branch))
        self.assertTrue(inspect.isclass(alphatwirl.roottree.BranchAddressManager))
        self.assertTrue(inspect.isclass(alphatwirl.roottree.Events))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.Analyzer))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.Component))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ComponentLoop))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ComponentReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.EventBuilderConfig))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.HeppyResult))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadCounter))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadVersionInfo))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblCounter))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblCounterLong))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblBrilCalc))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Reader))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Count))
        self.assertTrue(inspect.isclass(alphatwirl.summary.NextKeyComposer))
        self.assertTrue(inspect.isclass(alphatwirl.loop.Collector))
        self.assertTrue(inspect.isclass(alphatwirl.loop.CollectorComposite))
        self.assertTrue(inspect.isclass(alphatwirl.loop.DatasetIntoEventBuildersSplitter))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoop))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoopProgressReportWriter))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventsInDatasetReader))
        self.assertTrue(inspect.isclass(alphatwirl.loop.MPEventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.loop.NullCollector))
        self.assertTrue(inspect.isclass(alphatwirl.loop.ReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.BProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.NullProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressBar))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressPrint))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReport))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReportPickup))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReporter))
        self.assertTrue(inspect.isclass(alphatwirl.summary.BackrefMultipleArrayReader))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Count))
        self.assertTrue(inspect.isclass(alphatwirl.summary.KeyValueComposer))
        self.assertTrue(inspect.isclass(alphatwirl.summary.NextKeyComposer))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Reader))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Scan))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Sum))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Summarizer))
        self.assertTrue(inspect.isclass(alphatwirl.summary.WeightCalculatorOne))

##________________________________._________________________________||
