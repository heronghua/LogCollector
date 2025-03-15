#================================================================
# File Name: LogCollectManager.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 19:57:18 2025
#================================================================
#!/usr/bin/env python
import os
from LogType import LogType
from MainLogCollectRunner import MainLogCollectRunner
from ScreenRecordCollectRunner import ScreenRecordCollectRunner
from EventsLogCollectRunner import EventsLogCollectRunner
from CamMetadataDump import CamMetadataDump
from SysPropertyCollectRunner import SysPropertyCollectRunner

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

        #start all collect
        for runner in self.group:
            runner.start()

        pass

    def stopCollect(self):
        for runner in self.group:
            runner.stop()

        pass


if __name__ == "__main__":
    if not os.path.exists("out"):
        os.mkdir("out")
    collectManager = CollectManager()
    collectManager.startCollect(LogType.LOG_MAIN.value|LogType.LOG_EVENTS.value|LogType.SCREEN_RECORD.value|LogType.CAM_DUMP.value|LogType.PROPERTIES.value)

    input("Press Enter to stop:")

    collectManager.stopCollect()

