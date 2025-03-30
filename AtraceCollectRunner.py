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
        self.stopCmd = f"{self.adb_prefix} shell atrace --async_stop -o /data/local/tmp/atrace.output && {self.adb_prefix} pull /data/local/tmp/atrace.output {output_dir}/{log_file_name}"

if __name__ == "__main__":
    atraceCollectRunner = AtraceCollectRunner()
    atraceCollectRunner.start()
    input("Press Enter to stop:")
    atraceCollectRunner.stop()
