#!/bin/bash -x

clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks_export_data
INSTANCE_ID="i-5c7f3121"
# VNC server @ 64
export DISPLAY=:64
CURR_MONTH=$(date +'%Y%m')
IS_REQUESTED=$(python qb_export_data_request.py)
IS_MONTHEND=$(python /home/ubuntu/qboe/test_repo_2/utils/check_monthend.py)

# check if this is the instance id
if [ "$INSTANCE_ID" != "`curl -s http://169.254.169.254/latest/meta-data/instance-id`" ]; then
  echo "This is not SPOF_LASTPASS_DR.cascadeo.com. Aborting QuickBooks data dump."
  exit -1
fi

if [ "$IS_REQUESTED" == "REQUESTED" ]; then
  echo "Checking if an email was received."
  IS_EMAIL_FOUND=$(python qb_check_email.py)
  if [ "$IS_EMAIL_FOUND" == "FOUND" ]; then
    # check for existing dumps for the day
    export TZ=America/Los_Angeles
    PDT_DATE=$(date +'%Y%m%d')
    LS_RS=$(ls export_company_$PDT_DATE*.qbxml | wc -l)
    echo $LS_RS
    unset TZ
    if [ $LS_RS -eq 0 ]; then
      echo "Extracting export file for today."
      python qb_export_data.py
      EXPORT_FILE=$(ls -t export_company_$PDT_DATE*.qbxml | head -n 1)
      sed -i "s/&lt;/</g" $EXPORT_FILE
      sed -i "s/&gt;/>/g" $EXPORT_FILE
    else
      echo "File for this day exists already."
      exit 1
    fi
    exit 0
  else
    echo "Email re data export not found. Exiting with code 1"
    exit 1
  fi
else
  echo "Export not requested. Exiting with code 1"
  exit 1
fi

# archive dumps and log by monthend
if [ $IS_MONTHEND -eq 1 ]; then
  echo "It's monthend. Hence, dumps for this month will be backed up."
  tar czvf export_company_$CURR_MONTH.tar.gz export_company_$CURR_MONTH*.qbxml && rm -f export_company_$CURR_MONTH*.qbxml
  tar czvf qb_export_data_$CURR_MONTH.log.tar.gz qb_export_data.log && rm -f qb_export_data.log
  echo "Dumps archived to export_company_$CURR_MONTH.tar.gz."
  echo "Log archived to qb_export_data_$CURR_MONTH.log.tar.gz"
fi
