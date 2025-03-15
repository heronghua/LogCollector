#================================================================
# File Name: LogCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from CollectRunner import CollectRunner
import os
import subprocess

class LogCollectRunner(CollectRunner):

    def __init__(self, output_dir="out", log_file_name="main.log", device=None):
        super().__init__()
        self.output_file = os.path.join(output_dir, log_file_name)
        self.output = open(self.output_file,'w')
        self.cmd = f"{self.adb_prefix} logcat -b main"
        


    def start(self):
        self.process = subprocess.Popen(self.cmd,shell=True,stdout=self.output,stderr=subprocess.PIPE)
        
    def stop(self):
        self.process.terminate()
        self.output.close()
        
        

if __name__ == "__main__":
    logCollector = LogCollectRunner()
    logCollector.start()
    input("Press any key to continue:")
    logCollector.stop()
