#!/bin/bash

clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks_export_data
IS_REQUESTED=$(python qb_export_data_request.py)

if [ "$IS_REQUESTED" == "REQUESTED" ]; then
  IS_EMAIL_FOUND=$(python qb_check_email.py)
  if [ "$IS_EMAIL_FOUND" == "FOUND" ]; then
    echo "We can export the data now."
    exit 0
  else
    echo "Exiting with code 1"
    exit 1
  fi
else
  echo "Exiting with code 2"
  exit 2
fi
