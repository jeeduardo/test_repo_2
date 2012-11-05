#!/bin/bash
# "crontab -e" entry
# 0 2 * * * /home/ubuntu/qboe/test_repo_2/freshbooks/freshbooks-dump.sh
clear
# 08Oct2012 - archiving
CURR_MONTH=$(date +"%Y-%m")
declare -i IS_MONTHEND
IS_MONTHEND=$(python /home/ubuntu/qboe/test_repo_2/utils/check_monthend.py)

INSTANCE_ID="i-5c7f3121"
# check if this is the instance id
if [ "$INSTANCE_ID" != "`curl -s http://169.254.169.254/latest/meta-data/instance-id`" ]; then
  echo "This is not SPOF_LASTPASS_DR.cascadeo.com. Aborting FreshBooks data dump."
  exit -1
fi


# 08Oct2012
echo "Starting freshbooks dump script"
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
if [ $IS_MONTHEND -eq 1 ]; then
  echo "Archiving CSV backups for this month..."
  tar czvf freshbooks_dump_$CURR_MONTH.tar.gz QB-FreshbooksCascadeoStaging_$CURR_MONTH-*
  rm -rf QB-FreshbooksCascadeoStaging_$CURR_MONTH-*/
fi
exit 0
