#!/bin/bash -x

clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks
# VNC server @ 64
export DISPLAY=:64
python quickbooks-report-dump.py

exit 0
