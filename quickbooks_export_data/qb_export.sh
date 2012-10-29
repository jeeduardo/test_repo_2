#!/bin/bash -x

clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks_export_data
# VNC server @ 64
export DISPLAY=:64
IS_REQUESTED=$(python qb_export_data_request.py)

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
