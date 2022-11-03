



#!/bin/bash

bash -c 'python3 /home/pkh/src/pilap/lampserver.py > /tmp/blink_out.log 2>&1' &
#bash -c 'python /home/pi/python/pilamp/lampserver.py > /tmp/blink_out.log 2>&1' &

# startti rc.local:ista rivillä
#  home/pkh/src/pilap/startserver.sh
# 
