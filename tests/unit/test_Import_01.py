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
        self.assertTrue(inspect.isfunction(alphatwirl.aggregate.combine_MC_yields_in_datasets_into_xsec_in_processes))
        self.assertTrue(inspect.isfunction(alphatwirl.aggregate.stack_counts_categories))
        self.assertTrue(inspect.isfunction(alphatwirl.aggregate.sumOverCategories))

        self.assertTrue(inspect.isclass(alphatwirl.collector.CombineIntoPandasDataFrame))
        self.assertTrue(inspect.isclass(alphatwirl.collector.WritePandasDataFrameToFile))

    @unittest.skipUnless(hasROOT, "has no ROOT")
    def test_with_ROOT(self):
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.BEventBuilder))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.EventBuilder))

        self.assertTrue(inspect.isclass(alphatwirl.events.BEvents))
        self.assertTrue(inspect.isclass(alphatwirl.events.BranchAddressManagerForVector))

    def test_functions(self):
        self.assertTrue(inspect.isfunction(alphatwirl.mkdir_p))

    def test_classes(self):
        self.assertTrue(inspect.isclass(alphatwirl.loop.Collector))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Binning))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Echo))
        self.assertTrue(inspect.isclass(alphatwirl.binning.Round))
        self.assertTrue(inspect.isclass(alphatwirl.binning.RoundLog))
        self.assertTrue(inspect.isclass(alphatwirl.concurrently.CommunicationChannel))
        self.assertTrue(inspect.isclass(alphatwirl.collector.CombineIntoList))
        self.assertTrue(inspect.isclass(alphatwirl.collector.WriteListToFile))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Reader))
        self.assertTrue(inspect.isclass(alphatwirl.summary.Count))
        self.assertTrue(inspect.isclass(alphatwirl.summary.NextKeyComposer))
        self.assertTrue(inspect.isclass(alphatwirl.loop.Collector))
        self.assertTrue(inspect.isclass(alphatwirl.loop.CollectorComposite))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoop))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoopProgressReportWriter))
        self.assertTrue(inspect.isclass(alphatwirl.loop.EventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.loop.ReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.loop.MPEventLoopRunner))
        self.assertTrue(inspect.isclass(alphatwirl.events.Branch))
        self.assertTrue(inspect.isclass(alphatwirl.events.BranchAddressManager))
        self.assertTrue(inspect.isclass(alphatwirl.events.Events))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.Analyzer))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.Component))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ComponentLoop))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ComponentReaderComposite))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.HeppyResult))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadCounter))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.ReadVersionInfo))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblCounter))
        self.assertTrue(inspect.isclass(alphatwirl.heppyresult.TblComponentConfig))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressBar))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReport))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReporter))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.NullProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.BProgressMonitor))
        self.assertTrue(inspect.isclass(alphatwirl.progressbar.ProgressReportPickup))

##________________________________._________________________________||
