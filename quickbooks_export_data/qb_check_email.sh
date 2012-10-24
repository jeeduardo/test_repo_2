#!/bin/bash
clear
cd /home/ubuntu/qboe/test_repo_2/quickbooks_export_data
python qb_check_email.py > qb_check_email_$(date +'%Y%m%d').txt
