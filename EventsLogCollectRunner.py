#================================================================
# File Name: EventsLogCollectRunner.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 21:03:15 2025
#================================================================
#!/usr/bin/env python
from LogCollectRunner import LogCollectRunner
import os

class EventsLogCollectRunner(LogCollectRunner):

    def __init__(self, output_dir="out", log_file_name="events.log", device=None):
        super().__init__(output_dir,log_file_name,device)
        self.cmd = f"{self.adb_prefix} logcat -b events"

if __name__ == "__main__":
    eventsLogCollector = EventsLogCollectRunner()
    eventsLogCollector.start()
    input("Press Enter to stop:")
    eventsLogCollector.stop()
