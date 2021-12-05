#!/usr/bin/python3
#

import aiohttp
import asyncio
from time import sleep
import string
import argparse



parser = argparse.ArgumentParser()

parser.add_argument("-f","--file", help = "input file name")
parser.parse_args()
args= parser.parse_args()
if(args.file):
    myinfile=open(args.file,"r")
    mystring=myinfile.read()
    myprocstring=mystring.format("qqq","www")
    print(myprocstring)
else:
    print("No file")

