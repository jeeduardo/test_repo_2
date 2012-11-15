#!/bin/bash -x

clear
INSTANCE_ID="i-5c7f3121"

# check if this is the instance id
if [ "$INSTANCE_ID" != "`curl -s http://169.254.169.254/latest/meta-data/instance-id`" ]; then
  echo "This is not SPOF_LASTPASS_DR.cascadeo.com. Aborting QuickBooks data dump."
  exit -1
fi

cd /home/ubuntu/qboe/test_repo_2/quickbooks
# VNC server @ 64
export DISPLAY=:64
python quickbooks-report-dump.py

echo "Closing firefox session."
sleep 5
ps ax | grep firefox | awk '{print $1}' | xargs kill -9
exit 0
