#!/usr/bin/python3
#

#
# Macscanner must change for better
#

from subprocess import Popen, PIPE
from io import StringIO
import csv
import platform
import commondata
import os

import logging

log = logging.getLogger(__name__)
FORMAT="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
#logfilename = commondata.logpath+__file__+".log"

logfilename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(level=commondata.loglevel,format=FORMAT,datefmt="%H:%M:%S",filename=commondata.logpath+logfilename+".log")

from datetime import datetime
import set_client

Rasp ='14:dd:a9:2e:e5:63'
OivanKannykka = '44:91:60:64:b5:32'
mikataaon = '54:27:58:35:74:ae'
PetrinKannykka = 'a8:db:03:f8:03:42'
SarinA3 = '84:98:66:1c:35:55'

MACS =  [Rasp, OivanKannykka, mikataaon, PetrinKannykka, SarinA3]

MYNET ='192.168.100.1/24'

MAC_IN = 0
MAC_OUT = 1

if (commondata.pi==True):
    Scantime = 1800  # seconds, scanner wait time
    pingtime ='10'
else:
    Scantime = 40  # seconds, scanner wait time, for PC-testing
    pingtime ='1'



class terminal():
    def __init__(self,macin='00:00:00:00:00:00'):
        self.MAC=macin
        self.IP=''
        self.status=1

    def dump(self):
        log.debug("MAC: "+ self.MAC)
        log.debug('IP: '+ self.IP)
        log.debug('Status: '+ str(self.status))


class mynet():

    def __init__(self):
        self.terminals=[]
        for mac in MACS:
            self.terminals.append(terminal(mac))

    def scanmynet(self):
        pid = Popen(["nmap", "-sn", "-T4", MYNET], stdout=PIPE)
        nmapout = pid.communicate()[0]
        pid.terminate()

        pid = Popen(["arp", "-n"], stdout=PIPE)
        arpout = pid.communicate()[0]
        pid.terminate()

        s=arpout.decode()

        f = StringIO(str(s))
        reader = csv.reader(f, delimiter=' ', skipinitialspace = True)

        for maci in range(len(MACS)):
            self.terminals[maci].status = MAC_OUT


        for row in reader:
            if (row[1] != '(incomplete)'):
                for maci in range(len(MACS)):
                     if (self.terminals[maci].MAC==row[2]):
                         self.terminals[maci].IP = row[0]
                         #print("Ping " + self.terminals[maci].IP)
                         pingid = Popen(["ping", "-w"+pingtime,self.terminals[maci].IP], stdout=PIPE)
                         pingdata=pingid.communicate()[0]
                         #log.debug(pingdata)
                         self.terminals[maci].status=pingid.returncode
                         log.debug("Ping " + self.terminals[maci].IP + " - RetVal: " + str(pingid.returncode))
                         pingid.terminate()




        return(self.terminals)



class macscanner():
    def __init__(self):
        self.mymy=mynet()
        self.newscan=self.mymy.scanmynet()
        self.oldscan = self.newscan[:]

        self.netscans = []
        self.times=[]
        self.maxlen = 10

        self.term_statuses = [0] * len(MACS)
        self.old_statuses = [0] * len(MACS)
        self.new_statuses = [0] * len(MACS)
        self.datedscan =  [datetime.timestamp(datetime.now())]


    def MACIn(self,a=[1],b=[1]):
        for index in range(len(a)):
            if (a[index]==1 and b[index]==0):
                return(index)
        return(-1)

    def scan(self):

        self.Summary = [1] * len(MACS)


        self.datedscan = [datetime.timestamp(datetime.now())]
        log.debug("--------New scan--------")
        self.newscan = self.mymy.scanmynet()

        self.old_statuses = self.new_statuses[:]
        self.datedscan.append((self.old_statuses))     # list: [time, [list of scanresults]]
        self.netscans.append(self.datedscan)
        while ((self.netscans[len(self.netscans)-1][0] - self.netscans[0][0])>Scantime):
            self.netscans.pop(0)

        log.debug("Netscanlen = "+ str(len(self.netscans))+ " Diff = "+ str(self.netscans[len(self.netscans)-1][0] - self.netscans[0][0]))

        for maci in range(len(MACS)):
            self.new_statuses[maci] = self.newscan[maci].status


        for self.scanindex in range(len(self.netscans)):
            for self.terminal in range(len(MACS)):
                self.Summary[self.terminal] &= self.netscans[self.scanindex][1][self.terminal]



        self.macinval = self.MACIn(self.Summary,self.new_statuses)

        if (self.macinval>-1):
            log.info("MACIN! " + MACS[self.macinval])
            set_client.set_up()
        else:
            log.debug("NoChange")

if(__name__=="__main__"):

    log.info("---------Macscanner starts on "+platform.uname()[4]+"-----------")
    myscanner = macscanner()

    log.debug("---------Macscanner loop starts-----------")
    while(True):
        myscanner.scan()