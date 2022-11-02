import logging

FORMAT="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
logpath="/tmp/"
loglevel=logging.DEBUG


LampPort = 11111

import platform

plattis= platform.uname()[4]
if (plattis == 'x86_64'):
    pi = False
    TimeIncrement = 10  # Short moment for testing
    WorkingDir = "/home/petri/PycharmProjects/lampserver/"
else:
    if (plattis=='armv7l') or (plattis=='armv6l'):
        pi = True
        TimeIncrement = 600  # 10 minutes
        WorkingDir = "/home/pi/python/lampserver/"
    else:
        print("Alustaa ei löytynyt")
        exit(1)


#testmod2


