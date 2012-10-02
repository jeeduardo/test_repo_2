#!/bin/bash
clear
echo 'Starting freshbooks dump script'
# export DISPLAY=:99 && cd /home/earl/CASCADEO/15755/freshbooks_dump_v2 && /home/earl/CASCADEO/15755/freshbooks_dump_v2/freshbooks_clients.py
# check if vncserver on :64 is running
IS_VNC_RUNNING=$(ps aux | grep "Xtightvnc" | grep -v "color=auto")
if [ "$IS_VNC_RUNNING" != "" ]; then
  echo "Xtightvnc is running"
fi

export DISPLAY=:64 && cd /home/ubuntu/qboe/test_repo_2/freshbooks && ./freshbooks-dump.py
exit 0
