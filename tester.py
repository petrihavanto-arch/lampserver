#!/usr/bin/env python3
#

import aiohttp
import asyncio
from time import sleep

import logging

log = logging.getLogger(__name__)
FORMAT="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
logging.basicConfig(level=logging.DEBUG,format=FORMAT,datefmt="%H:%M:%S")



async def fetch(client):
    async with client.get('http://127.0.0.1:11111/set') as resp:
        assert resp.process_stat == 200
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)


def set_up():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.shutdown_asyncgens()


while True:
    set_up()
    sleep(15)
