#================================================================
# File Name: CamMetadataDump.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from LogCollectRunner import LogCollectRunner
import subprocess
import threading

class CamMetadataDump(LogCollectRunner):

    def __init__(self, output_dir="out", log_file_name="media.camera", device=None):
        super().__init__(output_dir,log_file_name,device)
        self.stopCmd = f"{self.adb_prefix} shell dumpsys media.camera"

    def stop(self):
        super().stop(self.output)
        
if __name__ == "__main__":
    camMetadataDump = CamMetadataDump()
    camMetadataDump.start()
    input("Press Enter to stop:")
    camMetadataDump.stop()
