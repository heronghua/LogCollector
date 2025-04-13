#================================================================
# File Name: LogCollectManager.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 19:57:18 2025
#================================================================
#!/usr/bin/env python
import os
import concurrent.futures
from LogType import LogType
from MainLogCollectRunner import MainLogCollectRunner
from ScreenRecordCollectRunner import ScreenRecordCollectRunner
from EventsLogCollectRunner import EventsLogCollectRunner
from CamMetadataDump import CamMetadataDump
from SysPropertyCollectRunner import SysPropertyCollectRunner
from AtraceCollectRunner import AtraceCollectRunner

class CollectManager:

    def __init__(self):
        self.group = []
        pass
        
    def startCollect(self, logs):
        if(logs & LogType.LOG_MAIN.value):
            self.group.append(MainLogCollectRunner())
        if(logs & LogType.LOG_EVENTS.value):
            self.group.append(EventsLogCollectRunner())
        if(logs & LogType.SCREEN_RECORD.value):
            self.group.append(ScreenRecordCollectRunner())
        if(logs & LogType.CAM_DUMP.value):
            self.group.append(CamMetadataDump())
        if(logs & LogType.PROPERTIES.value):
            self.group.append(SysPropertyCollectRunner())
        if(logs & LogType.SYS_TRACE.value):
            self.group.append(AtraceCollectRunner())

        #start all collect
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(runner.start) for runner in self.group]
            concurrent.futures.wait(futures)

    def stopCollect(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(runner.stop) for runner in self.group]
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    if not os.path.exists("out"):
        os.mkdir("out")
    collectManager = CollectManager()
    collectManager.startCollect(LogType.LOG_MAIN.value|LogType.LOG_EVENTS.value|LogType.SCREEN_RECORD.value|LogType.CAM_DUMP.value|LogType.PROPERTIES.value|LogType.PROPERTIES.value)

    input("Press Enter to stop:")

    collectManager.stopCollect()

