#================================================================
# File Name: LogType.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Mon Mar 10 20:02:47 2025
#================================================================
#!/usr/bin/env python
from enum import Enum

class LogType(Enum):
    LOG_MAIN = 1
    LOG_EVENTS = 2
    SCREEN_RECORD = 3
    SYS_TRACE = 4
    M_DUMP = 5

