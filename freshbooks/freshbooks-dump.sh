#!/bin/bash
# "crontab -e" entry
# 0 2 * * * /home/ubuntu/qboe/test_repo_2/freshbooks/freshbooks-dump.sh
clear
# 03Oct2012 - testing
CURR_DAY=$(date +%d)
CAL_DAY=$(echo `cal` | awk '{print $NF}')
CURR_MONTH=$(date +%Y-%m)
echo 'Starting freshbooks dump script'
# check if vncserver on :64 is running
IS_VNC_RUNNING=$(ps aux | grep "Xtightvnc" | grep -v "grep")
if [ "$IS_VNC_RUNNING" != "" ]; then
  echo "VNC Server is running. Proceeding with dump."
else
  echo "VNC Server is not running. Starting VNC Server..."
  vncserver :64
  echo "Proceeding with dump."
fi

export DISPLAY=:64 && cd /home/ubuntu/qboe/test_repo_2/freshbooks && ./freshbooks-dump.py
# 03Oct2012 - archive files
if [ $CURR_DAY -eq $CAL_DAY ]; then
  echo "Archiving CSV backups for this month..."
  tar czvf freshbooks_dump_$CURR_MONTH.tar.gz QB-FreshbooksCascadeoStaging_$CURR_MONTH-*
  rm -rf QB-FreshbooksCascadeoStaging_$CURR_MONTH-*/
fi
exit 0
