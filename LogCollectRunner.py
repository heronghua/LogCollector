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

    def __init__(self, output_dir="out", log_file_name="log.log", device=None):
        super().__init__()
        output_file = os.path.join(output_dir, log_file_name)
        self.output = open(output_file,'w')

    def runStartCmd(self):
        self.startProcess = subprocess.Popen(self.startCmd,shell=True,stdout=self.output,stderr=subprocess.PIPE)

