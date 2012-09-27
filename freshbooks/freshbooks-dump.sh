#!/bin/bash
clear
echo 'Ending any Xvfb sessions..'
ps aux | grep Xvfb | awk '{print 2}' | sudo xargs kill -9
rm -f /tmp/.X99-lock
echo 'Starting screen session'
/usr/bin/Xvfb :99 -ac &
echo 'Starting freshbooks dump script'
# export DISPLAY=:99 && cd /home/earl/CASCADEO/15755/freshbooks_dump_v2 && /home/earl/CASCADEO/15755/freshbooks_dump_v2/freshbooks_clients.py
export DISPLAY=:99 && cd /home/earl/CASCADEO/15755/freshbooks_dump_v2 && /home/earl/CASCADEO/15755/freshbooks_dump_v2/freshbooks-dump.py
echo 'Ending any Xvfb sessions..'
ps aux | grep Xvfb | awk '{print 2}' | sudo xargs kill -9
