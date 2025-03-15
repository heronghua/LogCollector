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
        self.device = device  # 添加设备参数
        self.adb_prefix = f"adb -s {device}" if device else "adb"

        self.output_file = os.path.join(output_dir, output_file_name)
        self.remote_output_file = f"/sdcard/{output_file_name}"
        self.START_CMD = f"{self.adb_prefix} shell screenrecord --size 720x1280 --bugreport {self.remote_output_file}"
        self.STOP_CMD = f"{self.adb_prefix} pull {self.remote_output_file} {self.output_file}"


    def start(self):
        try:
            #TODO 打开屏幕Touch 点
            subprocess.Popen(self.START_CMD, shell=True)
            print("Screen recording started...")
        except Exception as e:
            print(f"Error starting screen recording: {e}")

    def stop(self):
        try:
            # 发送终止信号
            self.run_adb_command("shell pkill -l INT screenrecord")

            # 轮询等待 screenrecord 进程退出
            for _ in range(10):  # 最长等待10秒
                result = self.run_adb_command("shell pidof screenrecord")
                if not result.stdout.strip():  # 进程已退出
                    break
                time.sleep(1)

            # 数据完整性保护
            self.run_adb_command("shell sync")
            subprocess.run(self.STOP_CMD, shell=True)

            print("Screen recording stopped and saved.")
        except Exception as e:
            print(f"Error stopping screen recording: {e}")

if __name__ == "__main__":
    output_dir = "out"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # 可通过命令行指定设备，如：python ScreenRecordCollectRunner.py emulator-5554
    import sys
    device = sys.argv[1] if len(sys.argv) > 1 else None

    runner = ScreenRecordCollectRunner(device=device)
    runner.start()
    input("按回车键停止录制")
    runner.stop()