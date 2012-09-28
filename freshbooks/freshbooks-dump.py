#!/usr/bin/python
# freshbooks_clients.py
# dump client csv from freshbooks
import ConfigParser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pdb
import os, re
# 06June2012 - enable logging
import logging
# 28Sep2012 - include freshbooks_functions
import freshbooks_functions
from freshbooks_functions import cfg


# 28Sep2012
FF = freshbooks_functions
# firefox profile
fp = FF.fp

# 06June2012
# logging config
logging.basicConfig(filename=os.getcwd() + '/freshbooks.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

# function to get CSV file
# don't wanna keep repeating myself
# @params p_disp_msg - message to display while downloading the file (i.e. 'downloading Tax Summary CSV (billed)...')
# @params p_driver - instance of the Firefox driver used to get the file
# @params p_pattern - pattern to use in displaying the name of the file downloaded and to be renamed
# @params p_url - url of file to download
# @params p_params - parameters to pass to the url used in downloading the file

def get_file(p_disp_msg, p_driver, p_pattern, p_url, p_params=''):
  global logging
  # print p_disp_msg
  logging.info(p_disp_msg)
  p_driver.get(p_url + p_params)
  # print 'File saved as %s' % get_csv_filename(p_pattern)
  logging.info('File saved as %s' % get_csv_filename(p_pattern))
  return 0

# use -lrt preferably or -rt
# if pattern left blank, it will get the name of latest csv file
def get_csv_filename(pattern=''):
  # file is non-existent
  #p = os.popen("ls -t wackstest-cascadeo" + pattern + "*.csv | head -1")
  # the pattern below (i.e. "Trial Josephson (Cascadeo)")should be stored in the .cfg file
  # p = os.popen("ls -t Trial\ Josephson\ \(Cascadeo\)" + pattern + "*.csv | head -1")
  p = os.popen("ls -t Staging\ Backup\ Cascadeo" + pattern + "*.csv | head -1")
  filename = p.readline().strip()
  p.close()
  return re.escape(filename)


logging.info('getting set configurations')
#cfg = ConfigParser.ConfigParser()
#cfg.read('freshbooks-dump.cfg')
print 'Backup dir. name = %s' % (cfg.get('settings', 'backup_dir_name'))


# 06June2012
# create backup directory
#backup_dirname = "Trial\ Josephson\ \(Cascadeo\)\ -\ " + datetime.now().strftime('%Y-%m-%d')
#backup_dirname = "Staging\ Backup\ Cascadeo\ -\ " + datetime.now().strftime('%Y-%m-%d')
backup_dirname_rs = os.system("mkdir " + FF.backup_dirname)

#sent_invoice_csv_url = url + cfg.get('export_urls', 'sent_invoice_csv_url')
#client_csv_url = url + cfg.get('export_urls', 'client_csv_url')
#staff_csv_url = cfg.get('export_urls', 'staff_csv_url')
sent_invoice_csv_url = FF.get_csv_url('sent_invoice_csv_url')
client_csv_url = FF.get_csv_url('client_csv_url')
staff_csv_url = FF.get_csv_url('staff_csv_url')

# 05Mar2012 - expenses (by category for now?) url
expenses_csv_url = FF.get_csv_url('expenses_by_category_url')

profit_loss_url = FF.get_csv_url('profit_loss_csv_url') # CHANGE variable name LATER please

tax_summary_csv_url = FF.get_csv_url('tax_summary_csv_url')
accounts_aging_csv_url = FF.get_csv_url('accounts_aging_csv_url')
payments_coll_csv_url = FF.get_csv_url('payments_coll_csv_url')
item_sales_csv_url = FF.get_csv_url('item_sales_csv_url')
tasks_inv_csv_url = FF.get_csv_url('tasks_inv_csv_url')
snail_mail_csv_url = FF.get_csv_url('snail_mail_csv_url')
time_to_pay_csv_url = FF.get_csv_url('time_to_pay_csv_url')
revenue_by_client_url = FF.get_csv_url('revenue_by_client_url')
user_summary_csv_url = FF.get_csv_url('user_summary_csv_url')
task_summary_csv_url = FF.get_csv_url('task_summary_csv_url')


# currency
ccy = cfg.get('settings', 'currency')


now = datetime.now()
# 4-digit and 2-digit year respectively
nowYear4Digit = str(now.year)
nowYear2Digit = str(now.strftime('%y'))


driver = webdriver.Firefox(firefox_profile=fp)
# print 'initializing freshbooks home page...'
logging.info('initializing freshbooks home page...')
driver.get(FF.url)
time.sleep(5)

logging.info('logging in as %s' % FF.username)
driver.find_element_by_id('username').click()
driver.find_element_by_id('username').send_keys(FF.username)
driver.find_element_by_id('password').click()
driver.find_element_by_id('password').send_keys(FF.pw)
# print driver.find_element_by_xpath("//input[@type='submit']")
driver.find_element_by_xpath("//input[@type='submit']")

#print driver.execute_script("document.getElementsByClassName('button-submit')[0].style.display='block';")
# print driver.find_elements_by_name('Submit')[2].click()
driver.find_elements_by_name('Submit')[2].click()

#
# temporary (28Feb2012) - Wacko
time.sleep(10)

get_file('downloading "Clients" CSV backup...', driver, 'Clients', client_csv_url, '')
FF.get_and_rename_file('Clients')

# 28Sep2012 - Josephson (TEMPORARY!)
time.sleep(10)
driver.quit()
exit()
# 28Sep2012
time.sleep(5)
get_file('downloading "Staff" CSV backup...', driver, 'Staff', staff_csv_url, '')
get_and_rename_file('Staff')

driver.find_element_by_id('nav-reports').click()

# NEXT course of action please?
#-Invoices (and its details) - Yes - both client invoices and received invoices as well as payment history 
#- Expenses 
#- Reports
# (Wacko) - like what type of reports?


# my comments - wacko
# Expenses - "broad" ones?
# Invoices - I can only see the ones "we" have issued, not the ones "we" had received
# Reports - like what type of reports?

# only thing I could do (probably for the meantime) 
# is to export the invoices we send to client/s
# url: https://wackstestcascadeo.freshbooks.com/menu.php?route=Report_InvoiceDetails&type=invoice&format=csv&type=invoice
# invoices for march are blank.. might need to set post data
# possible input fields to manipulate (form method is GET):
# date_start, date_end, date_option, route (set to 'Report_InvoiceDetails'), button name="submit"
# Question: since when did Cascadeo use FreshBooks? (or perhaps when was their first invoice recorded?)

time.sleep(10)

get_file('downloading sent invoices CSV backup...', driver, '_Invoice\ Details', sent_invoice_csv_url, '')
get_and_rename_file('_Invoice\ Details')


# ------------------------------------------
# expenses
# 05Mar2012 - wacko (T E M P O R A R Y   O N L Y ! ! !)

params = '&date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y') + '&group_by=category'
# 08Mar2012 - wacko (might need to modify this, this can be grouped into five fields actually - Category, Vendor, Client, Author, Project)
get_file('downloading expenses (by category) CSV backup...', driver, '_Expenses', expenses_csv_url, params)
get_and_rename_file('_Expenses')

# profit and loss - billed, exclude sales tax (_ProfitLoss.csv)
# convention
# billed - BI
# collected - CO
# tax excluded - TEX
# tax included - TIN
# billed, tax excluded - BI-TEX

get_file('downloading Profit & Loss CSV (billed, excluded sales tax)', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y='+now.strftime('%Y')+'&revenue=billed&expense_taxes=0')
get_and_rename_file('_ProfitLoss', '_BI-TEX')

# profit and loss - billed, include sales tax
get_file('downloading Profit & Loss CSV (billed, included sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' + now.strftime('%Y') + '&revenue=billed&expense_taxes=1')
get_and_rename_file('_ProfitLoss', '_BI-TIN')

# profit and loss - collected, exclude sales tax
get_file('downloading Profit & Loss CSV (collected, excluded sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' +now.strftime('%Y')+ '&revenue=collected&expense_taxes=0')
get_and_rename_file('_ProfitLoss', '_CO-TEX')


# profit and loss - collected, include sales tax
get_file('downloading Profit & Loss CSV (collected, included sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' + now.strftime('%Y') + '&revenue=collected&expense_taxes=1') 
get_and_rename_file('_ProfitLoss', '_CO-TIN')

## Tax Summary
# Tax summary - billed
# convention:
# BI - Billed
# CO - Collected
get_file('downloading Tax Summary CSV (billed)...', driver, '_TaxSummary'+ccy, tax_summary_csv_url, '&date_start=01/01/'+str(now.strftime('%y'))+'&date_end='+now.strftime('%m/%d/%y')+'&revenue=billed&currency='+ccy)
get_and_rename_file('_TaxSummary'+ccy, '_BI')

# Tax summary - collected
get_file('downloading Tax Summary CSV (collected)...', driver, '_TaxSummary'+ccy, tax_summary_csv_url, '&date_start=01/01/'+str(now.strftime('%y'))+'&date_end='+now.strftime('%m/%d/%y')+'&revenue=collected&currency='+ccy)
get_and_rename_file('_TaxSummary'+ccy, '_CO')


# Accounts aging
get_file('downloading Accounts Aging CSV...', driver, '_AccountsAging', accounts_aging_csv_url, '&end_date=' + now.strftime('%m/%d/%y'))
get_and_rename_file('_AccountsAging')

# Payments collected 
get_file('downloading Payments collected CSV...', driver, '_PaymentCollected', payments_coll_csv_url, '&start_date=' + now.strftime('01/01/%y') + '&end_date=' + now.strftime('%m/%d/%y'))
get_and_rename_file('_PaymentCollected')
# CONSIDER including the patterns like '_PaymentCollected' to configuration file
# we're not certain as to when or if FreshBooks will change their naming conventions

# Item sales
params = '&date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
print 'downloading Item sales CSV...'
driver.get(item_sales_csv_url)
print 'File saved as %s' % get_csv_filename('_Item Sales')
#print 'File saved as %s' % get_csv_filename()
get_and_rename_file(re.escape('_Item Sales'))

# Tasks invoiced
# _ProfitLoss and _TaxSummary files not yet renamed accdg to timestamp
# because of varying parameters passed to the reports
params = 'date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
print 'downloading Tasks invoiced CSV...'
driver.get(tasks_inv_csv_url + params)
print 'File saved as %s' % get_csv_filename()
get_and_rename_file(re.escape('_Invoiced Tasks'))


# Snail mail 
params = 'date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
print 'downloading Snail Mail CSV...'
driver.get(snail_mail_csv_url + params)
print 'File saved as %s' % get_csv_filename()
get_and_rename_file(re.escape('_Snail mail'))


# Time to pay - percentage of the invoices created
# HOW ABOUT a function of driver.get to this?
# print, driver.get, print file name, rename file
# conventions
# PER - percentage of the invoices created
# VAL - value
# CNT - count
get_file('downloading Time to pay (percentage of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=1')
get_and_rename_file(re.escape('_Time to pay'), '_PER')

# Time to Pay - value of the invoices created
get_file('downloading Time to pay (value of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=2')
get_and_rename_file(re.escape('_Time to pay'), '_VAL')

# Time to Pay - count of the invoices created
get_file('downloading Time to pay (count of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=3')
get_and_rename_file(re.escape('_Time to pay'), '_CNT')


# Revenue by Client - Total collected
# IF I DIDN'T pass a parameter for client[], how would FreshBooks interpret it? Find out!
# conventions:
# RBC - Revenue by Client
# TC - Total collected
# TO - Total outstanding
# TB - Total billed
# i.e. RBC-TC - Revenue by Client (Total collected)
get_file('downloading Revenue by Client (Total collected) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=1&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBC-TC')

# Revenue by Client - Total outstanding
get_file('downloading Revenue by Client (Total outstanding) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=2&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBC-TO')

# Revenue by Client - Total billed
get_file('downloading Revenue by Client (Total billed) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=3&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBC-TB')

# Revenue by Staff - Total Received (by invoice date)
# conventions:
# RBS - Revenue by Staff
# TRID - Total received by invoice date
# TRPD - Total received by payment date
# TO - Total outstanding
# TB - Total billed
# i.e. RBS-TO - Revenue by Staff (Total Outstanding)
get_file('downloading Revenue by Staff (Total Received by invoice date) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=1&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBS-TRID')
# you can use 'driver' as a global file(?)

# Revenue by Staff - Total Outstanding
get_file('downloading Revenue by Staff (Total Outstanding) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=2&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBS-TO')


# Revenue by Staff - Total Billed
get_file('downloading Revenue by Staff (Total Billed) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=3&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBS-TB')

# Revenue by Staff - Total Received (by payment date)
get_file('downloading Revenue by Staff (Total Received by payment date) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=4&submit=')
get_and_rename_file(re.escape('_Client Sales'), '_RBS-TRPD')

# WILL SKIP 'Recurring Revenue' --> Annual and Detailed for now (08Mar2012)

# User summary
# might use %2F instead of '/' ???
get_file('downloading User Summary CSV...', driver, '', user_summary_csv_url, 'date_start='+now.strftime('01/01/%y')+'&date_end='+now.strftime('%m/%d/%y')+'&team[]=&submit=')
get_and_rename_file('_UserSummary')

# Task summary
get_file('downloading User Summary CSV...', driver, '', task_summary_csv_url, 'start_date='+now.strftime('01/01/%y')+'&end_date='+now.strftime('%m/%d/%y')+'&task[]=&submit=')
get_and_rename_file('_TaskSummary')


time.sleep(15)
# type is "text/csv"
logging.info('Data has been exported. Ending program.')
driver.quit()
exit


# ------------------------------------------
# 05Mar2012 - TO DO:
# Exporting of Expenses and Reports
# Expenses by category url - https://wackstestcascadeo.freshbooks.com/menu.php?route=Report_Expenses&type=expense&format=csv&type=expense
# Are the POST data/s needed for the 'Expenses' by category export?
# AND HOW ABOUT The "OTHER" Invoices CSV export url? The one in Import & Export -> Comma Separated Values (CSV)??
# form method is GET
# so we can pass 'GET' parameters to the url (the driver.get function)
#
# have a function that will take a pattern (i.e. Staff, Invoices, Clients)
# to search for latest file (depending on pattern)
# and to rename that file
# R E M E M B E R ! ! !
# remember to send signal to KNOW if python script exited successfully or not
