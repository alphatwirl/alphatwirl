import AlphaTwirl
import unittest
import inspect

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
        self.assertTrue(inspect.isfunction(AlphaTwirl.Aggregate.combine_MC_yields_in_datasets_into_xsec_in_processes))
        self.assertTrue(inspect.isfunction(AlphaTwirl.Aggregate.stack_counts_categories))
        self.assertTrue(inspect.isfunction(AlphaTwirl.Aggregate.sumOverCategories))

        self.assertTrue(inspect.isclass(AlphaTwirl.Collector.CombineIntoPandasDataFrame))
        self.assertTrue(inspect.isclass(AlphaTwirl.Collector.WritePandasDataFrameToFile))

    @unittest.skipUnless(hasROOT, "has no ROOT")
    def test_with_ROOT(self):
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.BEventBuilder))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.EventBuilder))

        self.assertTrue(inspect.isclass(AlphaTwirl.Events.BEvents))
        self.assertTrue(inspect.isclass(AlphaTwirl.Events.BranchAddressManagerForVector))

    def test_functions(self):
        self.assertTrue(inspect.isfunction(AlphaTwirl.mkdir_p))

    def test_classes(self):
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.Collector))
        self.assertTrue(inspect.isclass(AlphaTwirl.Binning.Binning))
        self.assertTrue(inspect.isclass(AlphaTwirl.Binning.Echo))
        self.assertTrue(inspect.isclass(AlphaTwirl.Binning.Round))
        self.assertTrue(inspect.isclass(AlphaTwirl.Binning.RoundLog))
        self.assertTrue(inspect.isclass(AlphaTwirl.Concurrently.CommunicationChannel))
        self.assertTrue(inspect.isclass(AlphaTwirl.Collector.CombineIntoList))
        self.assertTrue(inspect.isclass(AlphaTwirl.Collector.WriteListToFile))
        self.assertTrue(inspect.isclass(AlphaTwirl.Summary.Reader))
        self.assertTrue(inspect.isclass(AlphaTwirl.Summary.Count))
        self.assertTrue(inspect.isclass(AlphaTwirl.Summary.NextKeyComposer))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.Collector))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.CollectorComposite))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.EventLoop))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.EventLoopProgressReportWriter))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.EventLoopRunner))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.ReaderComposite))
        self.assertTrue(inspect.isclass(AlphaTwirl.Loop.MPEventLoopRunner))
        self.assertTrue(inspect.isclass(AlphaTwirl.Events.Branch))
        self.assertTrue(inspect.isclass(AlphaTwirl.Events.BranchAddressManager))
        self.assertTrue(inspect.isclass(AlphaTwirl.Events.Events))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.Analyzer))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.Component))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.ComponentLoop))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.ComponentReaderComposite))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.HeppyResult))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.ReadComponentConfig))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.ReadCounter))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.ReadVersionInfo))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.TblCounter))
        self.assertTrue(inspect.isclass(AlphaTwirl.HeppyResult.TblComponentConfig))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.ProgressBar))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.ProgressMonitor))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.ProgressReport))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.ProgressReporter))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.NullProgressMonitor))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.BProgressMonitor))
        self.assertTrue(inspect.isclass(AlphaTwirl.ProgressBar.ProgressReportPickup))

##________________________________._________________________________||
