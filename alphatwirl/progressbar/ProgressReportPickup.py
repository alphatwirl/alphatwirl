# Tai Sakuma <tai.sakuma@cern.ch>
import multiprocessing
import time

##__________________________________________________________________||
class ProgressReportPickup(multiprocessing.Process):
    def __init__(self, queue, presentation):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.presentation = presentation
        self.lastWaitTime = 1.0 # [second]

    def run(self):
        self._run_until_the_end_order_arrives()
        self._run_until_reports_stop_coming()

    def _run_until_the_end_order_arrives(self):
        end_order_arrived = False
        while True:
            while not self.queue.empty():
                report = self.queue.get()
                if report is None: # the end order
                    end_order_arrived = True
                    continue
                self.presentation.present(report)
            if end_order_arrived: break

    def _run_until_reports_stop_coming(self):
        self._readTime()
        while self.presentation.nreports() > 0:
            if self._time() - self.lastTime > self.lastWaitTime: break
            while not self.queue.empty():
                report = self.queue.get()
                if report is None: continue
                self._readTime()
                self.presentation.present(report)

    def _time(self): return time.time()
    def _readTime(self): self.lastTime = self._time()

##__________________________________________________________________||
