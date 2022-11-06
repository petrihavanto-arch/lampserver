#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import platform

import commondata

local_logger=logging.getLogger(__name__)


plattis = platform.uname()[4]
if (plattis == 'x86_64'):
    pi = False
    local_logger.debug("--------------Running in PC----------------")
else:
    if (plattis == 'armv7l') or (plattis == 'armv6l'):
        pi = True
        local_logger.debug("--------------Running in Raspberry----------------")
    else:
        local_logger.debug("--------------Running in who-knows-where----------------")
        exit(1)


if (commondata.pi == True):
    import RPi.GPIO as GPIO

if (commondata.pi == True):
    GPIO.setmode(GPIO.BCM)


class relaycontroller():
    ctrl_port = 'Z'

    def __init__(self,portletter='A'):

        def PortA():
            self.on_pin = 20
            self.off_pin = 21

        def PortB():
            self.on_pin = 14
            self.off_pin = 25

        def PortC():
            self.on_pin = 15
            self.off_pin = 8

        def PortD():
            self.on_pin = 24
            self.off_pin = 23

        def PortIDFault():
            local_logger.info("Unknown port requested: " + portletter)
            self.on_pin = -1
            self.off_pin = -1


        self.ctrl_port = portletter

        {'A': PortA,
         'B': PortB,
         'C': PortC,
         'D': PortD}.get(portletter, PortIDFault)()

        if (commondata.pi ==True):
            GPIO.setup(self.on_pin, GPIO.OUT)
            GPIO.setup(self.off_pin, GPIO.OUT)

        local_logger.info("Varataan portti " + portletter)


    def switch_on(self):
        local_logger.info("Portti: " + self.ctrl_port + " Laite päälle.")
        if (commondata.pi ==True):
            GPIO.output(self.on_pin,True)
        time.sleep(0.5)
        if (commondata.pi ==True):
            GPIO.output(self.on_pin,False)

    def switch_off(self):
        local_logger.info("Portti: " + self.ctrl_port + " Laite pois.")
        if (commondata.pi ==True):
            GPIO.output(self.off_pin, True)
        time.sleep(0.5)
        if (commondata.pi ==True):
            GPIO.output(self.off_pin, False)


if(__name__ == "__main__"):
    mylamps = []
    lamplist ='ABCD'
    for i in range(len(lamplist)):
        mylamps.append(relaycontroller(lamplist[i]))

    print("Looppiin")
    local_logger.setLevel(logging.DEBUG)
    local_logger.propagate = False
#    logging.getLogger("__main__").setLevel(logging.DEBUG)
    while (True):
        for i in range(len(lamplist)):
            mylamps[i].switch_on()
            local_logger.debug(lamplist[i] + " paalle")
            print(lamplist[i] + " paalle")
            input()
            mylamps[i].switch_off()
            local_logger.debug(lamplist[i] + " pois")
            print(lamplist[i] + " pois")
            input()








