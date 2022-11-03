#!/usr/bin/env python3

from threading import Timer
import platform
import socket
import os
import logging

import commondata
import relaycontroller

pihavaloreleportti = 'A'

log = logging.getLogger(__name__)
logfilename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(level=commondata.loglevel,
                    format=commondata.FORMAT,
                    datefmt="%H:%M:%S",
                    filename=commondata.logpath+logfilename+".log")

from aiohttp import web


class RepeatedTimer(object):
    def __init__(self, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = 1
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class MyDownCounter(RepeatedTimer):

    def __init__(self,onfunct, offunct):
        self.timecount = 0
        self.onfunct=onfunct
        self.offunct=offunct
        self.cntr = RepeatedTimer(self.downcount)

    def downcount(self):
        if (self.timecount > 0):
            self.timecount -= 1
            if(self.timecount==0):
                self.offunct()

    def addtime(self,timetoadd = 1):
        if(self.timecount==0):
            self.onfunct()
        self.timecount += timetoadd

    def settime(self, timetoset=1):
        if(self.timecount==0):
            self.onfunct()
        self.timecount = timetoset

    def gettime(self):
        return(self.timecount)

    def stop(self):
 #       self.cntr.stop()
        self.offunct()
        self.timecount=0




class lampserver(object):

    def __init__(self,lampport=8080):
        log.info("-------------Lampserver starting---------------")
        self.mycounter = MyDownCounter(self.onfunction, self.offunction)
        self.mylamp = relaycontroller.relaycontroller(pihavaloreleportti)

        self.app = web.Application()
        self.app.add_routes([web.get('/stat', self.process_stat)])
        self.app.add_routes([web.get('/add', self.process_add)])
        self.app.add_routes([web.get('/set', self.process_set)])
        self.app.add_routes([web.get('/off', self.process_off)])

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.0.0.0', 0))
        web.run_app(self.app, port=lampport, host=s.getsockname()[0])


    def onfunction(self):
        log.debug("On")
        self.mylamp.switch_on()

    def offunction(self):
        log.debug("Off")
        self.mylamp.switch_off()

    async def process_add(self, request):
        self.mycounter.addtime(commondata.TimeIncrement)
        raise web.HTTPFound('/stat')

    async def process_set(self, request):
        self.mycounter.settime(commondata.TimeIncrement)
        raise web.HTTPFound('/stat')

    async def process_off(self, request):
        self.mycounter.stop()
        raise web.HTTPFound('/stat')

    async def process_stat(self, request):
        if(self.mycounter.gettime()==0):
                myinfile=open(commondata.WorkingDir+"html/Pihavalo-ohjain_off.htm","r")
                mystring=myinfile.read()
                myinfile.close()
                my_pagetext=mystring
                return web.Response(content_type='text/html',text=my_pagetext)

        time_left_mins = self.mycounter.gettime() // 60
        time_left_secs = self.mycounter.gettime() % 60
        myinfile=open(commondata.WorkingDir+"html/Pihavalo-ohjain_on.htm", "r")
        mystring=myinfile.read()
        myinfile.close()
        my_pagetext=mystring.format(time_left_mins,time_left_secs)
        return web.Response(content_type='text/html',
                            text=my_pagetext)

        #return web.Response(content_type='text/html', text=" <meta http-equiv=\"refresh\" content=\"1\"/> <h1> \n\nJaljella: " + time_left + "</h1>")


    async def up(self,request):
        self.mycounter.addtime()
        return web.Response(text=" Lisaaikaa: " + str(self.mycounter.gettime()))


if(__name__=="__main__"):

    log.info("---------Lampserver starts on "+platform.uname()[4]+"-----------")

    mylampserver=lampserver(commondata.LampPort)
