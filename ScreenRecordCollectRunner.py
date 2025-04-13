#================================================================
# File Name: ScreenRecordCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Sat Mar  8 20:17:00 2025
#================================================================
#!/usr/bin/env python

import os
import subprocess
import time
from CollectRunner import CollectRunner

class ScreenRecordCollectRunner(CollectRunner):

    def __init__(self, output_dir="out", output_file_name="screen_record.mp4", device=None):
        super().__init__()
        self.output_file = os.path.join(output_dir, output_file_name)
        remote_output_file = f"/sdcard/{output_file_name}"
        self.startCmd = f"{self.adb_prefix} shell screenrecord --size 720x1280 --bugreport {remote_output_file}"
        self.stopCmd = f"{self.adb_prefix} shell pkill -l INT screenrecord && {self.adb_prefix} shell sync && {self.adb_prefix} pull {remote_output_file} {self.output_file}"

if __name__ == "__main__":
    output_dir = "out"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # You can spicify deviceId eg. ScreenRecordCollectRunner.py emulator-5554
    import sys
    device = sys.argv[1] if len(sys.argv) > 1 else None

    runner = ScreenRecordCollectRunner(device=device)
    runner.start()
    input("Press any key to stop record")
    runner.stop()
