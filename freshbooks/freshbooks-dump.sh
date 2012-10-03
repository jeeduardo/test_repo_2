#!/bin/bash
# "crontab -e" entry
# 0 2 * * * /home/ubuntu/qboe/test_repo_2/freshbooks/freshbooks-dump.sh
clear
# 03Oct2012 - testing
CURR_DAY=$(date +%d)
CAL_DAY=$(echo `cal` | awk '{print $NF}')
TO_ARCHIVE=$(/home/ubuntu/qboe/test_repo_2/freshbooks/freshbooks_to_archive.py $CAL_DAY)
CURR_MONTH=$(date +%Y-%m)
echo 'Starting freshbooks dump script'
# export DISPLAY=:99 && cd /home/earl/CASCADEO/15755/freshbooks_dump_v2 && /home/earl/CASCADEO/15755/freshbooks_dump_v2/freshbooks_clients.py
# check if vncserver on :64 is running
IS_VNC_RUNNING=$(ps aux | grep "Xtightvnc" | grep -v "grep")
if [ "$IS_VNC_RUNNING" != "" ]; then
  echo "Xtightvnc is running"
else
  echo "Xtightvnc server must be started first!"
  exit -1
fi

export DISPLAY=:64 && cd /home/ubuntu/qboe/test_repo_2/freshbooks && ./freshbooks-dump.py
# 03Oct2012 - archive files
if [ $CURR_DAY -eq $CAL_DAY ]; then
  echo "Archiving CSV backups for this month..."
  tar czvf FRESHBOOKS_ARC_$CURR_MONTH.tar.gz QB-FreshbooksCascadeoStaging_$CURR_MONTH-*
  rm -rf QB-FreshbooksCascadeoStaging_$CURR_MONTH-*/
fi
exit 0
