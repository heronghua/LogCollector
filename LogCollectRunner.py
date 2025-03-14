#================================================================
# File Name: LogCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 20:58:12 2025
#================================================================
#!/usr/bin/env python
import subprocess

class LogCollectRunner:

    def __init__(self):

        pass

    def start(self):

        pass
        
    def run_adb_command(self, cmd):
        """统一执行 adb 命令，减少重复代码"""
        full_cmd = f"{self.adb_prefix} {cmd}"
        return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

    def stop(self):
        
        pass

        
