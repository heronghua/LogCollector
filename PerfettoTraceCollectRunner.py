#================================================================
# File Name: PerfettoTraceCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Sun Apr  6 20:18:55 2025
#================================================================
#!/usr/bin/env python

from CollectRunner import CollectRunner
import os
import threading
import subprocess
from Logger import Log
log = Log()

CONFIG = """
buffers: {
  size_kb: 10240
  fill_policy: RING_BUFFER
}
data_sources: {
  config {
    name: "android.log"
  }
}
write_into_file: true
"""

class PerfettoTraceCollectRunner(CollectRunner):

    def __init__(self, output_dir="out", log_file_name="trace_output.perfetto-trace", device=None,config=CONFIG):
        super().__init__(output_dir,log_file_name,device)
        self.startCmd = f"{self.adb_prefix} shell perfetto --txt --config - -o /sdcard/trace_output.perfetto-trace"
        #self.stopCmd = f"{self.adb_prefix} shell pkill -l INT perfetto"
        self.stopCmd = f"{self.adb_prefix} pull /sdcard/trace_output.perfetto-trace {output_dir}/{log_file_name}"
        self.config = config

    def runStartCmd(self):
        log.d(f"PerfettoTraceCollectRunner [runStartCmd] + {self.startCmd} \n============================= {self.config} \n===============================")
        self.startProcess = subprocess.Popen(self.startCmd,stdin=subprocess.PIPE,shell=True, text=True)
        self.startProcess.stdin.write(self.config)
        self.startProcess.stdin.flush()
        log.d(f"PerfettoTraceCollectRunner [runStartCmd] - {self.startProcess}")
        return self.startProcess

    def runStopCmd(self):
        #subprocess.run(self.stopCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log.d(f"PerfettoTraceCollectRunner [runStopCmd]  pulling perfetto trace file")
        subprocess.run(self.stopCmd,shell=True,check=True)
        log.d(f"PerfettoTraceCollectRunner [runStopCmd] - ")

if __name__ == "__main__":
    perfettoTraceCollectRunner = PerfettoTraceCollectRunner()
    perfettoTraceCollectRunner.start()
    input("Press Enter to stop:")
    perfettoTraceCollectRunner.stop()
