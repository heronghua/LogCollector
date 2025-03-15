#================================================================
# File Name: AtraceCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from CollectRunner import CollectRunner
import os

class AtraceCollectRunner(CollectRunner):

    def __init__(self, output_dir="out", log_file_name="atrace.html", device=None):
        super().__init__(output_dir,log_file_name,device)
        #TODO impl
        self.cmd = f"{self.adb_prefix} atrace --async start"
        #TODO impl

if __name__ == "__main__":
    atraceCollectRunner = AtraceCollectRunner()
    atraceCollectRunner.start()
    input("Press Enter to stop:")
    atraceCollectRunner.stop()
