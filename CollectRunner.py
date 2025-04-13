#================================================================
# File Name: CollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 20:58:12 2025
#================================================================
#!/usr/bin/env python
import subprocess
import threading

class CollectRunner:

    def __init__(self,output_dir="out",log_file_name="default",device=None):
        self.device = device  # device id 
        self.adb_prefix = f"adb -s {device}" if device else "adb"
        self.startCmd = None
        self.stopCmd = None
        self.startProcess = None
        self.stopProcess = None

    def runAdbCommand(self,cmd):
        full_cmd = f"{self.adb_prefix} {cmd}"
        return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

    def start(self):
        if self.startCmd is not None:
            subprocess.Popen(self.startCmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def stop(self,out_put=None):
        if self.startProcess is not None:
            self.startProcess.terminate()
            self.startProcess.wait()

        if self.stopCmd is not None:
            if out_put is not None:
                output=out_put
            else:
                output=subprocess.PIPE
            self.stopProcess=subprocess.Popen(self.stopCmd,shell=True,stdout=output,stderr=subprocess.PIPE)
            self.stopProcess.wait()
