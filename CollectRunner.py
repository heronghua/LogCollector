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
        self.startThread = None
        self.stopThread = None
        self.startProcess = None
        self.stopProcess = None

    # real impl of start
    def runStartCmd(self):
        return subprocess.Popen(self.startCmd,shell=True)

    # real impl of stop
    def runStopCmd(self):
        subprocess.run(self.stopCmd,shell=True)

    def runAdbCommand(self,cmd):
        full_cmd = f"{self.adb_prefix} {cmd}"
        return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

    # set up a thread to run a subprocess
    def start(self):
        if self.startCmd is not None:
            self.startThread = threading.Thread(target=self.runStartCmd)
            self.startThread.setName("StartThread")
            self.startThread.start()

    # set up a thread to run a subprocess
    def stop(self):
        if self.startProcess is not None:
            self.startProcess.terminate()
            self.startProcess.wait()
            pass

        if self.stopCmd is not None:
            self.stopThread = threading.Thread(target=self.runStopCmd)
            self.stopThread.setName("StopThread")
            self.stopThread.start()
