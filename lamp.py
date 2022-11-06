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

pihavalo_socket = 11111
pihavalo_ohjain_releportti = 'A'
pihavalo_on_html = "html/Pihavalo-ohjain_on.htm"
pihavalo_off_html = "html/Pihavalo-ohjain_off.htm"


def main():
    args = proccmdline.proccmdline()
    if vars(args)['debug']:
        loglevel_here=logging.DEBUG
    else:
        loglevel_here = logging.INFO

    logging.getLogger().setLevel(loglevel_here)

    mylampserver = relayserver.relayserver(lampport=pihavalo_socket,
                                         releportti=pihavalo_ohjain_releportti,
                                         on_html=pihavalo_on_html,
                                         off_html=pihavalo_off_html)


if __name__ == '__main__':
    main()
