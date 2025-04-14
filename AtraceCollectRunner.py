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

    def __init__(self, output_dir="out", log_file_name="atrace", device=None,categories="gfx view sched binder_driver binder_lock camera"):
        super().__init__(output_dir,log_file_name,device)
        log_file_name = self.generateAtraceFileName()
        self.startCmd = f"{self.adb_prefix} shell atrace --async_start -c -b 16384 {categories}"
        self.stopCmd  = f"{self.adb_prefix} shell atrace --async_stop  -o /data/local/tmp/{log_file_name}"
        self.pullCmd  = f"{self.adb_prefix} pull /data/local/tmp/{log_file_name} {output_dir}/{log_file_name}"

    def generateAtraceFileName(self):
        model = subprocess.run([f'{adb_prefix}','shell','getprop','ro.product.model'],stdout=subprocess.PIPE,text=True).stdout.strip()
        build_id = subprocess.run([f'{adb_prefix}','shell','getprop','ro.build.id'],stdout=subprocess.PIPE,text=True).stdout.strip()
        build_version = subprocess.run([f'{adb_prefix}','shell','getprop','ro.build.version.release'],stdout=subprocess.PIPE,text=True).stdout.strip()
        record_time = subprocess.run([f'{adb_prefix}','shell','date','+%Y%m%d%H%M%S'],stdout=subprocess.PIPE,text=True).stdout.strip()
        return f"trace-{model}-{build_id}-{build_version}-{record_time}"

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
