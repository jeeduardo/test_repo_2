test_repo_2
===========

2nd test repo


Repo for FreshBooks/QuickBooks dump script

Divided into 2 folders:

freshbooks - contains scripts for backing up data from FreshBooks. 
quickbooks - contains scripts for backing up data from QuickBooks.

Cron job settings:
This is to be run as a daily cron job during non-working hours.

For FreshBooks:

0 2 * * * /home/ubuntu/qboe/test_repo_2/freshbooks/freshbooks-dump.sh


For QuickBooks:
<< insert crontab -l schedules here >>
0 3 * * * /home/ubuntu/qboe/test_repo_2/quickbooks/dump_casc_qboe_wrapper.sh

Dependencies:
selenium - for scraping the FreshBooks and QuickBooks web pages to get the data needed.
