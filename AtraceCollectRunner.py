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

    def __init__(self, output_dir="out", log_file_name="atrace", device=None,categories="camera gfx disk"):
        super().__init__(output_dir,log_file_name,device)
        self.cmd = f"{self.adb_prefix} shell atrace --async_start {categories}"
        self.stopCmd = f"{self.adb_prefix} shell atrace --async_stop -z -o /data/local/tmp/atrace.output && {self.adb_prefix} pull /data/local/tmp/atrace.output {output_dir}/{log_file_name}"
        
    def start(self):
        thread = threading.Thread(target=subprocess.run, args=(self.cmd,), kwargs={'shell': True})
        thread.start()
    
    def stop(self):
        thread = threading.Thread(target=subprocess.run, args=(self.stopCmd,), kwargs={'shell': True})
        thread.start()

if __name__ == "__main__":
    atraceCollectRunner = AtraceCollectRunner()
    atraceCollectRunner.start()
    input("Press Enter to stop:")
    atraceCollectRunner.stop()
