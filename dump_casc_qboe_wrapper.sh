#!/bin/sh
# backup data from quickbooks online plus
clear
cd /var/www/qboe/trunk/cascadeo_qb_dump
# 29Aug2012 - Josephson (%H-%M-%S is temporary)
DATE_TODAY=$(date +"%Y-%m-%d-%H-%M-%S")
echo $DATE_TODAY
mkdir dump_quickbooks_$DATE_TODAY

php dump_casc_qboe.php
mv outfile_*_$DATE_TODAY_* dump_quickbooks_$DATE_TODAY/
tar czvf dump_quickbooks_$DATE_TODAY\.tar.gz dump_quickbooks_$DATE_TODAY/
rm -rf dump_quickbooks_$DATE_TODAY/
