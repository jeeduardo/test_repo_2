#!/usr/bin/python
# freshbooks_clients.py
# dump client csv from freshbooks
import ConfigParser
import selenium
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

# logging config
logging.basicConfig(filename=os.getcwd() + '/freshbooks.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

logging.info('getting set configurations')
#print 'Backup dir. name = %s' % (cfg.get('settings', 'backup_dir_name'))

backup_dirname_rs = os.system("mkdir " + FF.backup_dirname)
print "CSVs to be saved under %s" %(FF.backup_dirname)
logging.info("CSVs to be saved under %s" %(FF.backup_dirname.decode('string_escape')))

sent_invoice_csv_url = FF.get_csv_url('sent_invoice_csv_url')
# 03Oct2012 - download XLS version of sent invoices
sent_invoice_xls_url = FF.get_csv_url('sent_invoice_xls_url')
# 02Oct2012 - "header" of sent invoices
invoice_head_csv_url = FF.get_csv_url('invoice_head_csv_url')
# 02Oct2012
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
recurring_rev_annual_url = FF.get_csv_url('recurring_rev_annual_url')
recurring_rev_detailed_url = FF.get_csv_url('recurring_rev_detailed_url')

# currency
ccy = cfg.get('settings', 'currency')

now = datetime.now()

driver = webdriver.Firefox(firefox_profile=fp)
# print 'initializing freshbooks home page...'
logging.info('initializing freshbooks home page...')
driver.get(FF.url)
time.sleep(5)

logging.info('logging in as %s' % FF.username)
try:
  driver.find_element_by_id('username').click()
  driver.find_element_by_id('username').send_keys(FF.username)
  driver.find_element_by_id('password').click()
  driver.find_element_by_id('password').send_keys(FF.pw)
  # print driver.find_element_by_xpath("//input[@type='submit']")
  driver.find_element_by_xpath("//input[@type='submit']")
  #print driver.execute_script("document.getElementsByClassName('button-submit')[0].style.display='block';")
  # print driver.find_elements_by_name('Submit')[2].click()
  driver.find_elements_by_name('Submit')[2].click()
except selenium.common.exceptions.NoSuchElementException:
  import traceback
  err_msg = "Either network speed is TOO SLOW or such element doesn't exist in the page. Please check the site manually."
  logging.error(traceback.format_exc())
  logging.error(err_msg)
  print err_msg
  exit(1)
except Exception:
  import traceback
  tb = traceback.format_exc()
  logging.error(tb)
  print tb
  exit(1)

time.sleep(10)

FF.get_file('downloading "Clients" CSV backup...', driver, 'Clients', client_csv_url, '')
FF.get_and_rename_file('Clients')

time.sleep(5)
FF.get_file('downloading "Staff" CSV backup...', driver, 'Staff', staff_csv_url, '')
FF.get_and_rename_file('Staff')

driver.find_element_by_id('nav-reports').click()

# my comments - wacko
# Expenses - "broad" ones?
## Invoices - I can only see the ones "we" have issued, not the ones "we" had received
# Reports - like what type of reports?

# only thing I could do (probably for the meantime) 
# is to export the invoices we send to client/s
# url: https://wackstestcascadeo.freshbooks.com/menu.php?route=Report_InvoiceDetails&type=invoice&format=csv&type=invoice
# invoices for march are blank.. might need to set post data
# possible input fields to manipulate (form method is GET):
# date_start, date_end, date_option, route (set to 'Report_InvoiceDetails'), button name="submit"
# Question: since when did Cascadeo use FreshBooks? (or perhaps when was their first invoice recorded?)

time.sleep(10)

FF.get_file('downloading sent invoices CSV backup...', driver, '_Invoice\ Details', sent_invoice_csv_url, '')
FF.get_and_rename_file('_Invoice\ Details')

# 02Oct2012 - get the "header" of the entries from sent_invoice_csv_url
FF.get_file('downloading sent invoices header CSV...', driver, 'Invoices', invoice_head_csv_url, '')
FF.get_and_rename_file('Invoices')

params = '&date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y') + '&group_by=category'
# 08Mar2012 - wacko (might need to modify this, this can be grouped into five fields actually - Category, Vendor, Client, Author, Project)
FF.get_file('downloading expenses (by category) CSV backup...', driver, '_Expenses', expenses_csv_url, params)
FF.get_and_rename_file('_Expenses')

# profit and loss - billed, exclude sales tax (_ProfitLoss.csv)..below are the conventions:
# billed - BI
# collected - CO
# tax excluded - TEX
# tax included - TIN
# billed, tax excluded - BI-TEX

FF.get_file('downloading Profit & Loss CSV (billed, excluded sales tax)', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y='+now.strftime('%Y')+'&revenue=billed&expense_taxes=0')
FF.get_and_rename_file('_ProfitLoss', '_BI-TEX')

# profit and loss - billed, include sales tax
FF.get_file('downloading Profit & Loss CSV (billed, included sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' + now.strftime('%Y') + '&revenue=billed&expense_taxes=1')
FF.get_and_rename_file('_ProfitLoss', '_BI-TIN')

# profit and loss - collected, exclude sales tax
FF.get_file('downloading Profit & Loss CSV (collected, excluded sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' +now.strftime('%Y')+ '&revenue=collected&expense_taxes=0')
FF.get_and_rename_file('_ProfitLoss', '_CO-TEX')


# profit and loss - collected, include sales tax
FF.get_file('downloading Profit & Loss CSV (collected, included sales tax)...', driver, '_ProfitLoss', profit_loss_url, '&period=yearly&yearly_m=12&yearly_y=' + now.strftime('%Y') + '&revenue=collected&expense_taxes=1') 
FF.get_and_rename_file('_ProfitLoss', '_CO-TIN')

## Tax Summary
# Tax summary - billed
# convention:
# BI - Billed
# CO - Collected
FF.get_file('downloading Tax Summary CSV (billed)...', driver, '_TaxSummary'+ccy, tax_summary_csv_url, '&date_start=01/01/'+str(now.strftime('%y'))+'&date_end='+now.strftime('%m/%d/%y')+'&revenue=billed&currency='+ccy)
FF.get_and_rename_file('_TaxSummary'+ccy, '_BI')

# Tax summary - collected
FF.get_file('downloading Tax Summary CSV (collected)...', driver, '_TaxSummary'+ccy, tax_summary_csv_url, '&date_start=01/01/'+str(now.strftime('%y'))+'&date_end='+now.strftime('%m/%d/%y')+'&revenue=collected&currency='+ccy)
FF.get_and_rename_file('_TaxSummary'+ccy, '_CO')


# Accounts aging
FF.get_file('downloading Accounts Aging CSV...', driver, '_AccountsAging', accounts_aging_csv_url, '&end_date=' + now.strftime('%m/%d/%y'))
FF.get_and_rename_file('_AccountsAging')

# Payments collected 
FF.get_file('downloading Payments collected CSV...', driver, '_PaymentCollected', payments_coll_csv_url, '&start_date=' + now.strftime('01/01/%y') + '&end_date=' + now.strftime('%m/%d/%y'))
FF.get_and_rename_file('_PaymentCollected')
# CONSIDER including the patterns like '_PaymentCollected' to configuration file
# we're not certain as to when or if FreshBooks will change their naming conventions

# 01Oct2012 - use functions from FF
# Item sales
params = '&date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
FF.get_file('downloading Item sales CSV...', driver, re.escape('_Item Sales'), item_sales_csv_url, params)
FF.get_and_rename_file(re.escape('_Item Sales'))

# Tasks invoiced
# _ProfitLoss and _TaxSummary files not yet renamed accdg to timestamp
# because of varying parameters passed to the reports
params = 'date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
FF.get_file('downloading Tasks invoiced CSV...', driver, re.escape('_Invoiced Tasks'), tasks_inv_csv_url, params)
FF.get_and_rename_file(re.escape('_Invoiced Tasks'))
 
# Snail mail 
params = 'date_start=' + now.strftime('01/01/%y') + '&date_end=' + now.strftime('%m/%d/%y')
FF.get_file('downloading Snail Mail CSV...', driver, re.escape('_Snail mail'), snail_mail_csv_url, params)
FF.get_and_rename_file(re.escape('_Snail mail'))


# Time to pay - percentage of the invoices created
# conventions
# PER - percentage of the invoices created
# VAL - value
# CNT - count
FF.get_file('downloading Time to pay (percentage of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=1')
FF.get_and_rename_file(re.escape('_Time to pay'), '_PER')

# Time to Pay - value of the invoices created
FF.get_file('downloading Time to pay (value of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=2')
FF.get_and_rename_file(re.escape('_Time to pay'), '_VAL')

# Time to Pay - count of the invoices created
FF.get_file('downloading Time to pay (count of the invoices created) CSV...', driver, '', time_to_pay_csv_url, '&show=3')
FF.get_and_rename_file(re.escape('_Time to pay'), '_CNT')


# Revenue by Client - Total collected
# IF I DIDN'T pass a parameter for client[], how would FreshBooks interpret it? Find out!
# conventions:
# RBC - Revenue by Client
# TC - Total collected
# TO - Total outstanding
# TB - Total billed
# i.e. RBC-TC - Revenue by Client (Total collected)
FF.get_file('downloading Revenue by Client (Total collected) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=1&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBC-TC')

# Revenue by Client - Total outstanding
FF.get_file('downloading Revenue by Client (Total outstanding) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=2&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBC-TO')

# Revenue by Client - Total billed
FF.get_file('downloading Revenue by Client (Total billed) CSV...', driver, '', revenue_by_client_url, '&year='+now.strftime('%Y')+'&client[]=sales=3&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBC-TB')

# Revenue by Staff - Total Received (by invoice date)
# conventions:
# RBS - Revenue by Staff
# TRID - Total received by invoice date
# TRPD - Total received by payment date
# TO - Total outstanding
# TB - Total billed
# i.e. RBS-TO - Revenue by Staff (Total Outstanding)
FF.get_file('downloading Revenue by Staff (Total Received by invoice date) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=1&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBS-TRID')
# you can use 'driver' as a global file(?)

# Revenue by Staff - Total Outstanding
FF.get_file('downloading Revenue by Staff (Total Outstanding) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=2&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBS-TO')


# Revenue by Staff - Total Billed
FF.get_file('downloading Revenue by Staff (Total Billed) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=3&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBS-TB')

# Revenue by Staff - Total Received (by payment date)
FF.get_file('downloading Revenue by Staff (Total Received by payment date) CSV...', driver, '', revenue_by_client_url, 'year='+now.strftime('%Y')+'&team[]=&sales=4&submit=')
FF.get_and_rename_file(re.escape('_Client Sales'), '_RBS-TRPD')

# 01Oct2012 - Recurring Revenue CSV reports (no params for now)
FF.get_file('downloading Recurring Revenue (Annual) CSV...', driver, re.escape('_Recurring revenue - Annual'), recurring_rev_annual_url)
FF.get_and_rename_file(re.escape('_Recurring revenue - Annual'))
#FF.get_and_rename_file...

FF.get_file('downloading Recurring Revenue (Detailed) CSV...', driver, re.escape('_Recurring revenue - Detailed'), recurring_rev_detailed_url)
FF.get_and_rename_file(re.escape('_Recurring revenue - Detailed'))

# User summary
# might use %2F instead of '/' ???
FF.get_file('downloading User Summary CSV...', driver, '', user_summary_csv_url, 'date_start='+now.strftime('01/01/%y')+'&date_end='+now.strftime('%m/%d/%y')+'&team[]=&submit=')
FF.get_and_rename_file('_UserSummary')

# Task summary
FF.get_file('downloading User Summary CSV...', driver, '', task_summary_csv_url, 'start_date='+now.strftime('01/01/%y')+'&end_date='+now.strftime('%m/%d/%y')+'&task[]=&submit=')
FF.get_and_rename_file('_TaskSummary')

time.sleep(15)
# type is "text/csv"
time.sleep(5)
driver.find_element_by_id('nav-log-out').click()
logging.info('Data has been exported. Ending program.')
driver.quit()
exit(0)


# ------------------------------------------
# 05Mar2012 - TO DO:
# Exporting of Expenses and Reports
# Expenses by category url - https://wackstestcascadeo.freshbooks.com/menu.php?route=Report_Expenses&type=expense&format=csv&type=expense
# Are the POST data/s needed for the 'Expenses' by category export?
# AND HOW ABOUT The "OTHER" Invoices CSV export url? The one in Import & Export -> Comma Separated Values (CSV)??
