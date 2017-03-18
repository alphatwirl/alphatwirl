import alphatwirl
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
        self.assertTrue(inspect.isfunction(alphatwirl.Aggregate.combine_MC_yields_in_datasets_into_xsec_in_processes))
        self.assertTrue(inspect.isfunction(alphatwirl.Aggregate.stack_counts_categories))
        self.assertTrue(inspect.isfunction(alphatwirl.Aggregate.sumOverCategories))

        self.assertTrue(inspect.isclass(alphatwirl.Collector.CombineIntoPandasDataFrame))
        self.assertTrue(inspect.isclass(alphatwirl.Collector.WritePandasDataFrameToFile))

    @unittest.skipUnless(hasROOT, "has no ROOT")
    def test_with_ROOT(self):
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.BEventBuilder))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.EventBuilder))

        self.assertTrue(inspect.isclass(alphatwirl.Events.BEvents))
        self.assertTrue(inspect.isclass(alphatwirl.Events.BranchAddressManagerForVector))

    def test_functions(self):
        self.assertTrue(inspect.isfunction(alphatwirl.mkdir_p))

    def test_classes(self):
        self.assertTrue(inspect.isclass(alphatwirl.Loop.Collector))
        self.assertTrue(inspect.isclass(alphatwirl.Binning.Binning))
        self.assertTrue(inspect.isclass(alphatwirl.Binning.Echo))
        self.assertTrue(inspect.isclass(alphatwirl.Binning.Round))
        self.assertTrue(inspect.isclass(alphatwirl.Binning.RoundLog))
        self.assertTrue(inspect.isclass(alphatwirl.Concurrently.CommunicationChannel))
        self.assertTrue(inspect.isclass(alphatwirl.Collector.CombineIntoList))
        self.assertTrue(inspect.isclass(alphatwirl.Collector.WriteListToFile))
        self.assertTrue(inspect.isclass(alphatwirl.Summary.Reader))
        self.assertTrue(inspect.isclass(alphatwirl.Summary.Count))
        self.assertTrue(inspect.isclass(alphatwirl.Summary.NextKeyComposer))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.Collector))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.CollectorComposite))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.EventLoop))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.EventLoopProgressReportWriter))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.EventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.ReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.Loop.MPEventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.Events.Branch))
        self.assertTrue(inspect.isclass(alphatwirl.Events.BranchAddressManager))
        self.assertTrue(inspect.isclass(alphatwirl.Events.Events))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.Analyzer))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.Component))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.ComponentLoop))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.ComponentReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.HeppyResult))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.ReadComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.ReadCounter))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.ReadVersionInfo))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.TblCounter))
        self.assertTrue(inspect.isclass(alphatwirl.HeppyResult.TblComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.ProgressBar))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.ProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.ProgressReport))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.ProgressReporter))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.NullProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.BProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.ProgressBar.ProgressReportPickup))

##________________________________._________________________________||
