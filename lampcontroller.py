#!/usr/bin/python3
# -*- coding: utf-8 -*-



import time
import os
import logging
import commondata
log = logging.getLogger(__name__)

logfilename = os.path.splitext(os.path.basename(__file__))[0]

logging.basicConfig(level=commondata.loglevel,format=commondata.FORMAT,datefmt="%H:%M:%S",filename=commondata.logpath+logfilename+".log")


import platform

plattis= platform.uname()[4]
if (plattis == 'x86_64'):
    pi = False
    log.debug("--------------Running in PC----------------")
else:
    if (plattis=='armv7l'):
        pi = True
        log.debug("--------------Running in Raspberry----------------")
    else:
        log.debug("--------------Running in who-knows-where----------------")
        exit(1)


if (commondata.pi == True):
    import RPi.GPIO as GPIO

if (commondata.pi == True):
    GPIO.setmode(GPIO.BCM)


class lampcontroller():

    def __init__(self,portletter='A'):

        def PortB():
            self.on_pin = 14
            self.off_pin =15


        def PortA():
            self.on_pin = 20
            self.off_pin =21

        def PortC():
            self.on_pin = 25
            self.off_pin =8

        def PortD():
            self.on_pin = 24
            self.off_pin =23

        def PortIDFault():
            log.info("Unknown port requested: "+ portletter)
            self.on_pin = -1
            self.off_pin = -1




        # setdict={'A':PortA,
        #          'B':PortB,
        #          'C':PortC,
        #          'D':PortD}.get(portletter)()

        {'A':PortA,'B':PortB,
         'C':PortC,'D':PortD}.get(portletter, PortIDFault)()

        if (commondata.pi ==True):
            GPIO.setup(self.on_pin,GPIO.OUT)
            GPIO.setup(self.off_pin,GPIO.OUT)


    def switch_on(self):
        log.debug("Lamp on.")
        if (commondata.pi ==True):
            GPIO.output(self.on_pin,True)
        time.sleep(2)
        if (commondata.pi ==True):
            GPIO.output(self.on_pin,False)

    def switch_off(self):
        log.debug("Lamp off.")
        if (commondata.pi ==True):
            GPIO.output(self.off_pin, True)
        time.sleep(2)
        if (commondata.pi ==True):
            GPIO.output(self.off_pin, False)


if(__name__== "__main__"):
    mylamps=[]
    lamplist='ABCD'
    for i in range(len(lamplist)):
        mylamps.append(lampcontroller(lamplist[i]))



    while (True):
        for i in range(len(lamplist)):
            mylamps[i].switch_on()
            time.sleep(1)
            mylamps[i].switch_off()
            time.sleep(1)








