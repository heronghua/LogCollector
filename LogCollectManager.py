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

class LogCollectManager:

    def __init__(self):
        self.group = []
        pass
        
    def startCollect(self, logs):

        if(logs & LogType.LOG_MAIN.value):
            self.group.append(MainLogCollectRunner())
        if(logs & LogType.LOG_EVENTS.value):
            pass
        if(logs & LogType.SCREEN_RECORD.value):
            self.group.append(ScreenRecordCollectRunner())

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
    logCollectManager = LogCollectManager()
    logCollectManager.startCollect(LogType.LOG_MAIN.value|LogType.LOG_EVENTS.value|LogType.SCREEN_RECORD.value)

    input("Press Enter to stop:")

    logCollectManager.stopCollect()

