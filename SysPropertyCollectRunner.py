#================================================================
# File Name: SysPropertyCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from LogCollectRunner import LogCollectRunner
import subprocess

class SysPropertyCollectRunner(LogCollectRunner):

    def __init__(self, output_dir="out", log_file_name="properties", device=None):
        super().__init__(output_dir,log_file_name,device)
        self.cmd = f"{self.adb_prefix} shell getprop"

if __name__ == "__main__":
    sysPropertyCollectRunner = SysPropertyCollectRunner()
    sysPropertyCollectRunner.start()
    input("Press Enter to stop:")
    sysPropertyCollectRunner.stop()
