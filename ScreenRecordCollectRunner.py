#================================================================
# File Name: ScreenRecordCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Sat Mar  8 20:17:00 2025
#================================================================
#!/usr/bin/env python

import os
import subprocess
from LogCollectRunner import LogCollectRunner

class ScreenRecordCollectRunner(LogCollectRunner):

    def start(self,output_file="/sdcard/screenrecord.mp4"):
        self.remote_file_path = output_file
        self.local_file_path = "out/screen_record.mp4"
        cmd = ["adb","shell","screenrecord","--size","720x1280",output_file]
        process = subprocess.Popen(cmd,shell=True)
        return process

    def stop(self):
        stopCmd= f"adb shell \"pkill -l INT screenrecord && while [[ $(ps -A -Z|grep -E screenrecord) != '' ]]; do sleep 1; done \"&& adb pull {self.remote_file_path} {self.local_file_path}"
        subprocess.run(stopCmd,shell=True)
        pass
        

# 1. LogConnectManager.
# 2. LogConnectRunner 
# 3. manager deliver shared subprocess for no returned shell command.
# 4. Runner has start stop method
# 5. manager handle join
if __name__ == "__main__":
    if not os.path.exists("out"):
        os.mkdir("out")
        pass
    runner = ScreenRecordCollectRunner()
    runner.start()
    input("按回车键停止录制")
    runner.stop()


