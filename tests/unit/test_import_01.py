# Tai Sakuma <tai.sakuma@gmail.com>
import inspect
import pytest

import alphatwirl

##__________________________________________________________________||
has_no_pandas = False
try:
    import pandas
except ImportError:
    has_no_pandas = True

##__________________________________________________________________||
has_no_ROOT = False
try:
    import ROOT
except ImportError:
    has_no_ROOT = True

##__________________________________________________________________||
@pytest.mark.skipif(has_no_pandas, reason="has no pandas")
def test_with_pandas():
    assert inspect.isclass(alphatwirl.collector.ToDataFrameWithDatasetColumn)
    assert inspect.isclass(alphatwirl.collector.WritePandasDataFrameToFile)

@pytest.mark.skipif(has_no_ROOT, reason="has no ROOT")
def test_with_ROOT():
    assert inspect.isclass(alphatwirl.roottree.BEvents)
    assert inspect.isclass(alphatwirl.roottree.BranchAddressManager)
    assert inspect.isclass(alphatwirl.roottree.BranchAddressManagerForVector)
    assert inspect.isclass(alphatwirl.heppyresult.EventBuilder)
    assert inspect.isclass(alphatwirl.heppyresult.EventBuilderConfigMaker)
    assert inspect.isclass(alphatwirl.heppyresult.TblBranch)
    assert inspect.isclass(alphatwirl.heppyresult.TblTree)

def test_functions():
    assert inspect.isfunction(alphatwirl.mkdir_p)
    assert inspect.isfunction(alphatwirl.configure.build_counter_collector_pair)
    assert inspect.isfunction(alphatwirl.configure.build_progressMonitor_communicationChannel)

def test_classes():
    assert inspect.isclass(alphatwirl.binning.Binning)
    assert inspect.isclass(alphatwirl.binning.Echo)
    assert inspect.isclass(alphatwirl.binning.Round)
    assert inspect.isclass(alphatwirl.binning.RoundLog)
    assert inspect.isclass(alphatwirl.binning.Combine)
    assert inspect.isclass(alphatwirl.collector.ToTupleListWithDatasetColumn)
    assert inspect.isclass(alphatwirl.collector.WriteListToFile)
    assert inspect.isclass(alphatwirl.concurrently.CommunicationChannel)
    assert inspect.isclass(alphatwirl.concurrently.CommunicationChannel0)
    assert inspect.isclass(alphatwirl.concurrently.TaskPackage)
    assert inspect.isclass(alphatwirl.concurrently.TaskPackageDropbox)
    assert inspect.isclass(alphatwirl.concurrently.MultiprocessingDropbox)
    assert inspect.isclass(alphatwirl.concurrently.SubprocessRunner)
    assert inspect.isclass(alphatwirl.concurrently.WorkingArea)
    assert inspect.isclass(alphatwirl.concurrently.HTCondorJobSubmitter)
    assert inspect.isclass(alphatwirl.configure.TableConfigCompleter)
    assert inspect.isclass(alphatwirl.configure.TableFileNameComposer)
    assert inspect.isclass(alphatwirl.roottree.Branch)
    assert inspect.isclass(alphatwirl.roottree.Events)
    assert inspect.isclass(alphatwirl.heppyresult.Analyzer)
    assert inspect.isclass(alphatwirl.heppyresult.Component)
    assert inspect.isclass(alphatwirl.heppyresult.ComponentLoop)
    assert inspect.isclass(alphatwirl.heppyresult.ComponentReaderComposite)
    assert inspect.isclass(alphatwirl.heppyresult.EventBuilderConfig)
    assert inspect.isclass(alphatwirl.heppyresult.HeppyResult)
    assert inspect.isclass(alphatwirl.heppyresult.ReadComponentConfig)
    assert inspect.isclass(alphatwirl.heppyresult.ReadCounter)
    assert inspect.isclass(alphatwirl.heppyresult.ReadVersionInfo)
    assert inspect.isclass(alphatwirl.heppyresult.TblCounter)
    assert inspect.isclass(alphatwirl.heppyresult.TblComponentConfig)
    assert inspect.isclass(alphatwirl.heppyresult.TblCounterLong)
    assert inspect.isclass(alphatwirl.heppyresult.TblBrilCalc)
    assert inspect.isclass(alphatwirl.summary.Reader)
    assert inspect.isclass(alphatwirl.summary.Count)
    assert inspect.isclass(alphatwirl.summary.NextKeyComposer)
    assert inspect.isclass(alphatwirl.loop.Collector)
    assert inspect.isclass(alphatwirl.loop.CollectorComposite)
    assert inspect.isclass(alphatwirl.loop.DatasetIntoEventBuildersSplitter)
    assert inspect.isclass(alphatwirl.loop.EventLoop)
    assert inspect.isclass(alphatwirl.loop.EventLoopProgressReportWriter)
    assert inspect.isclass(alphatwirl.loop.EventLoopRunner)
    assert inspect.isclass(alphatwirl.loop.EventsInDatasetReader)
    assert inspect.isclass(alphatwirl.loop.MPEventLoopRunner)
    assert inspect.isclass(alphatwirl.loop.NullCollector)
    assert inspect.isclass(alphatwirl.loop.ReaderComposite)
    assert inspect.isclass(alphatwirl.progressbar.BProgressMonitor)
    assert inspect.isclass(alphatwirl.progressbar.NullProgressMonitor)
    assert inspect.isclass(alphatwirl.progressbar.ProgressBar)
    assert inspect.isclass(alphatwirl.progressbar.ProgressMonitor)
    assert inspect.isclass(alphatwirl.progressbar.ProgressMonitor)
    assert inspect.isclass(alphatwirl.progressbar.ProgressPrint)
    assert inspect.isclass(alphatwirl.progressbar.ProgressReport)
    assert inspect.isclass(alphatwirl.progressbar.ProgressReportPickup)
    assert inspect.isclass(alphatwirl.progressbar.ProgressReporter)
    assert inspect.isclass(alphatwirl.summary.BackrefMultipleArrayReader)
    assert inspect.isclass(alphatwirl.summary.Count)
    assert inspect.isclass(alphatwirl.summary.KeyValueComposer)
    assert inspect.isclass(alphatwirl.summary.NextKeyComposer)
    assert inspect.isclass(alphatwirl.summary.Reader)
    assert inspect.isclass(alphatwirl.summary.Scan)
    assert inspect.isclass(alphatwirl.summary.Sum)
    assert inspect.isclass(alphatwirl.summary.Summarizer)
    assert inspect.isclass(alphatwirl.summary.WeightCalculatorOne)

##________________________________._________________________________||
