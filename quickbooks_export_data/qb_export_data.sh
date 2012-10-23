#!/bin/bash


clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks_export_data
CHECK_EMAIL_RESPONSE=$(python qb_check_email.py)

CURR_DATE=$(date +'%Y%m%d')
CURR_MONTH=$(date +'%Y%m')
IS_MONTHEND=$(python /home/ubuntu/qboe/test_repo_2/utils/check_monthend.py)

if [ "$CHECK_EMAIL_RESPONSE" == "FOUND" ]; then
  export DISPLAY=:64
  ./qb_export_data.py
  EXPORT_FILE=$(ls -t export_company_$CURR_DATE_*.qbxml | head -n 1)
  sed -i "s/&lt;/</g" $EXPORT_FILE
  sed -i "s/&gt;/>/g" $EXPORT_FILE
else
  echo "No export request made today. Requesting"
  python qb_export_data_request.py
  exit 1
fi

# archive dumps by monthend
if [ $IS_MONTHEND -eq 1 ]; then
  echo "It's monthend. Hence, dumps for this month will be backed up."
  tar czvf export_company_$CURR_MONTH.tar.gz export_company_$CURR_MONTH*.qbxml
  echo "Dumps archived to export_company_$CURR_MONTH.tar.gz."
fi

exit 0
