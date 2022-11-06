#!/usr/bin/env python3

import relayserver
import logging
import os

import commondata
import proccmdline


log = logging.getLogger(__name__)
logfilename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(level=commondata.loglevel,
                    format=commondata.FORMAT,
                    datefmt="%H:%M:%S",
                    filename=commondata.logpath+logfilename+".log")

puhallin_socket = 11112
puhallin_ohjain_releportti = 'A'
puhallin_on_html = "html/puhallin-ohjain_on.htm"
puhallin_off_html = "html/puhallin-ohjain_off.htm"


def main():
    args = proccmdline.proccmdline()
    if vars(args)['debug']:
        loglevel_here = logging.DEBUG
    else:
        loglevel_here = logging.INFO

    logging.getLogger("relayserver").setLevel(loglevel_here)

    if(commondata.pi):
        my_timeincrement = 1800
    else:
        my_timeincrement = commondata.TimeIncrement *2

    mydryerserver = relayserver.relayserver(lampport=puhallin_socket,
                                         releportti=puhallin_ohjain_releportti,
                                         on_html=puhallin_on_html,
                                         off_html=puhallin_off_html,
                                         time_increment=my_timeincrement)


if __name__ == '__main__':
    main()
