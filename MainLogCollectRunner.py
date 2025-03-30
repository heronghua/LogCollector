#================================================================
# File Name: MainLogCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from LogCollectRunner import LogCollectRunner
import os

class MainLogCollectRunner(LogCollectRunner):

    def __init__(self, output_dir="out", log_file_name="main.log", device=None):
        super().__init__(output_dir,log_file_name,device)
        self.startCmd = f"{self.adb_prefix} logcat -b main"

if __name__ == "__main__":
    mainLogCollector = MainLogCollectRunner()
    mainLogCollector.start()
    input("Press Enter to stop:")
    mainLogCollector.stop()
