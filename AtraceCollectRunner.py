#================================================================
# File Name: AtraceCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from CollectRunner import CollectRunner
import os
import threading
import subprocess

class AtraceCollectRunner(CollectRunner):

    def __init__(self, output_dir="out", log_file_name="atrace", device=None,categories="gfx view sched binder_driver binder_lock camera gfx disk"):
        super().__init__(output_dir,log_file_name,device)
        self.startCmd = f"{self.adb_prefix} shell atrace --async_start -c -b 16384 {categories}"
        self.stopCmd = f"{self.adb_prefix} shell atrace --async_stop -o /data/local/tmp/atrace.output"
        self.pullCmd = f"{self.adb_prefix} pull /data/local/tmp/atrace.output {output_dir}/{log_file_name}"

    def runStartCmd(self):
        return subprocess.run(self.startCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def runStopCmd(self):
        subprocess.run(self.stopCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subprocess.run(self.pullCmd,shell=True)

    def stop(self):
        if self.stopCmd is not None:
            self.stopThread = threading.Thread(target=self.runStopCmd)
            self.stopThread.setName("StopThread")
            self.stopThread.start()

if __name__ == "__main__":
    atraceCollectRunner = AtraceCollectRunner()
    atraceCollectRunner.start()
    input("Press Enter to stop:")
    atraceCollectRunner.stop()
