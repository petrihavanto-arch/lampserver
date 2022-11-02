#!/usr/bin/env python3

import os
import logging
import commondata
log = logging.getLogger(__name__)
logfilename = os.path.splitext(os.path.basename(__file__))[0]
FORMAT="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
logging.basicConfig(level=commondata.loglevel,format=commondata.FORMAT,datefmt="%H:%M:%S",filename=commondata.logpath+logfilename+".log")

import aiohttp
import asyncio
from time import sleep

async def fetch(client):
    async with client.get('http://127.0.0.1:11111/add') as resp:
        #assert resp.process_stat == 200
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        log.debug("Set_client messaged")


def set_up():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# while True:
#     set_up()
#     sleep(15)
