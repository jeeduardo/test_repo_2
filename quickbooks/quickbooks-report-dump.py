#!/usr/bin/python
from selenium import webdriver
from datetime import datetime
import time
import os
import re
import ConfigParser
import logging
import platform

# 04Sep2012 - Josephson
# print dots . . .  to screen with given no. of seconds
# and also with message to display
def show_loading(p_seconds = 60, p_msg_while_waiting=''):
  print p_msg_while_waiting
  loading_cmd = ''
  for i in range(1, p_seconds+1):
    loading_cmd = loading_cmd + "echo -n '.'; sleep 1; "
#    print '.',
#    time.sleep(1)
  os.system(loading_cmd)
  print

def find_click(p_by='id', p_string='', p_send_keys='', p_seconds=0, p_msg_while_waiting='Loading'):
  global driver
  try:
    if p_by == 'id' or p_by == 'name':
      p_element = driver.find_element(p_by, p_string)
    else:
      print 'No element to find. Exiting...'
      exit()
  
    p_element.click()
    if p_send_keys <> '':
      p_element.send_keys(p_send_keys)
  
    if p_seconds > 0:
      show_loading(p_seconds, p_msg_while_waiting)
  except:
    import traceback
    # print traceback.format_exc()
    logging.error(traceback.format_exc())
    exit()

# 25Sep2012 - function to reload 'Report List' page
# go to 'Reports'
# go to 'Report List'
# load content

def reload_report_list():
  global driver
  print 'reloading "Report List"'
  find_click('id', 'nav6', '', 10, "Getting reports")
  find_click('id', 'nav601', '', 10, "Going to 'Report List'")
  driver.switch_to_default_content()
  home_frames = driver.find_elements_by_tag_name('iframe')
  driver.switch_to_frame(home_frames[0]) # since the page was reloaded

# switch to the frame where the menu/s and link/s can be found
def switch_frame():
  global driver
  # below 'print' is TEMPORARY
  print "switching to menu/link frame..."
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])

# 05Sep2012 - enable logging
# 25Sep2012 - use os.sep for directory separator
#logging.basicConfig(filename=os.getcwd() + os.sep + 'quickbooks_dump.log', level=logging.INFO, format='%(asctime) %(levelname)s : %(message)s')
logging.basicConfig(filename='quickbooks-report-dump.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

print "Setting up logging..."
# 04Sep2012 - get configurations
cfg = ConfigParser.ConfigParser()
cfg.read('quickbooks-report-dump.cfg')

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
ppword = cfg.get('credentials', 'ppword')

show_when_starting = cfg.get('prefs', 'show_when_starting')
if show_when_starting == 0:
  bool_show_when_starting = False
else:
  bool_show_when_starting = True

download_dir = cfg.get('prefs', 'download_dir')
save_to_disk = cfg.get('prefs', 'save_to_disk_immed')
#24Oct2012 - dirname
dirname = cfg.get('prefs', 'dirname')

# 24Sep2012 - get command named used to move/rename file(s) and DIRECTORY separator
# move - for windows
# mv - for linux/unix
mv = cfg.get('prefs', 'move_command')
sep = os.sep

# print mv
# create download director
datetime_now = datetime.now()
download_dir_full_path = download_dir + sep + dirname + datetime_now.strftime('%Y-%m-%d_%H%M')

# function to move file to target directory
def move_report_xls(report_name_prefix):
  global mv, download_dir_download_dir_full_path, datetime_now
  mv_cmd = "%s -v $(ls -t %s/report*.xls | head -n1) %s/%s_%s.xls" %(mv, download_dir, download_dir_full_path, report_name_prefix, datetime_now.strftime('%Y-%m-%d_%H%M'))
  logging.info(mv_cmd)
  return os.system(mv_cmd)

logging.info("creating download directory %s" %(download_dir_full_path))
os.system("mkdir %s" %(download_dir_full_path))

# get report - D.R.Y
def get_report(report_link_id, p_send_keys, p_seconds, report_name, date_macro_name, report_name_prefix):
  global driver
  try:
    print "Getting report named \"%s\"" %(report_name)
    reload_report_list()
    find_click('id', report_link_id, p_send_keys, p_seconds, "Getting \"%s\" report" %(report_name))
    switch_frame()
    if (date_macro_name <> ""):
      date_macro = driver.find_element_by_id(date_macro_name)
      date_macro.find_element_by_xpath("//option[@value='all']").click()
      driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
      show_loading(10, "Running report")
      switch_frame()

    driver.find_element_by_id('button_id_b5_excel_small.gif').click()
    logging.info("Getting Excel version of \"%s\" report" %(report_name))
    show_loading(5, "Getting Excel version of \"%s\" report" %(report_name))
    # move file
    move_report_xls(report_name_prefix)
    time.sleep(3)
  except:
    import traceback
    logging.error(traceback.format_exc())
  return 0
# set Firefox profile
logging.info("Loading Firefox profile...")
fp = webdriver.FirefoxProfile()
#fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting", False) # False
fp.set_preference("browser.download.dir", download_dir)#"C:\Users\josephson\Downloads")
#fp.set_preference("browser.download.dir", os.getcwd())
# 03Sept2012 - Josephson (file type="application/vnd.ms-excel")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", save_to_disk) #"application/vnd.ms-excel")

driver = webdriver.Firefox(firefox_profile=fp)
driver.get(url)
# 31Aug2012 - Josephson (testing something on clicking QBOE links)
# 23Oct2012 - temporary
logging.info("Loading QuickBooks")
# 23Oct2012 - temporary
logging.info("Loading %s" %(url))
show_loading(10, "Loading %s" % (url))
#/home/ubuntu/qboe/test_repo_2/quickbooks

logging.info("Logging in as %s" % (username))
# 04Sep2012 - Josephson (testing the _find_it function)
find_click('name', 'login', username, 2)

find_click('name', 'password', ppword, 2)
#driver.find_element_by_id('LoginButton').click()
# reducing waiting time to 30 as network speed is A-OK
find_click('id', 'LoginButton', '', 30, "Logging in and loading home page. ")


# go to first frame, click the 'Reports' tab
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0])
show_loading(10)
# 'Reports' tab

#driver.find_element_by_id('nav6').click() 
#show_loading(10, "Getting reports")
find_click('id', 'nav6', '', 10, "Getting reports")

# the 'Report List' submenu
# driver.find_element_by_id('nav601').click()
find_click('id', 'nav601', '', 10, "Going to 'Report List'")

#show_loading(10, "Getting the Banking reports")
logging.info("Getting the Banking reports")

# use get_report instead
# Deposit Details
get_report('DEPOSIT_DETAIL_reportListLink_Banking', '', 10, "Deposit Details", 'date_macro', "deposit_details") 

# find_click('id', 'category_BANKING', '', 2, "Getting the Banking reports")
# 24Oct2012 - temporary
reload_report_list()

# Journal
get_report('JOURNAL_reportListLink_Accountant & Taxes', '', 10, "Journal", 'date_macro', "journals")

# Profit & Loss
get_report('PANDL_reportListLink_Company', '', 10, "Profit & Loss", '', "profit_loss")

# Profit & Loss Detail
get_report('PANDL_DET_reportListLink_Company', '', 10, "Profit & Loss Detail", '', "profit_loss_detail")

# Balance Sheet
get_report('BAL_SHEET_reportListLink_Company', '', 10, "Balance Sheet", '', "balance_sheet")

# Balance Sheet Summary
get_report('BAL_SHEET_SUM_reportListLink_Company', '', 10, "Balance Sheet Summary", '', "balance_sheet_summary")

# Statement of Cash Flows
get_report('CASH_FLOW_reportListLink_Company', '', 10, "Statement of Cash Flows", '', "statement_cash_flows")

# A/R Aging
get_report('AR_AGING_reportListLink_Customers', '', 10, "A/R Aging Summary", 'date_macro', "ar_aging_summary")

# A/R Aging Detail
get_report('AR_AGING_DET_reportListLink_Customers', '', 10, "A/R Aging Detail", 'date_macro', "ar_aging_detail")

# Customer Balance Summary
get_report('CUST_BAL_reportListLink_Customers', '', 10, "Customer Balance Summary", 'date_macro', "customer_balance_summary")

# Customer Balance Detail
get_report('CUST_BAL_DET_reportListLink_Customers', '', 10, "Customer Balance Detail", '', "customer_balance_detail")

# Collections
get_report('COLLECTIONS_reportListLink_Customers', '', 10, "Collections", 'date_macro', "collections")

# Income by Customer Summary
get_report('CUST_INC_reportListLink_Customers', '', 10, "Income by Customer Summary", '', "income_by_cust_summary")

# Transaction List by Customer
get_report('TX_LIST_BY_CUST_reportListLink_Customers', '', 10, "Transaction List by Customer", 'date_macro', "txn_list_by_customer")

# Sales by Customer Summary
get_report('CUST_SALES_reportListLink_Customers', '', 10, "Sales by Customer Summary", 'date_macro', "sales_by_customer_summary")

# Sales by Customer Detail
get_report('CUST_SALES_DET_reportListLink_Customers', '', 10, "Sales by Customer Detail", 'date_macro', "sales_by_customer_detail")

# Invoice List
get_report('INVOICE_LIST_reportListLink_Customers', '', 10, "Invoice List", 'date_macro', "invoice_list")

# Statement List
get_report('STATEMENT_INVOICE_reportListLink_Customers', '', 10, "Statement List", 'stmtdate_macro', "statement_list")

# Sales by Product/Service Summary
get_report('ITEM_SALES_reportListLink_Sales', '', 10, "Sales by Product/Service Summary", 'date_macro', "sales_product_service_summary")

# Sales by Product/Service Detail
get_report('ITEM_SALES_DET_reportListLink_Sales', '', 10, "Sales by Product/Service Detail", 'date_macro', "sales_product_service_detail")

# logging out
# time.sleep(10)
# switch_frame()
# driver.find_element_by_link_text('Sign Out').click()
# time.sleep(5)
# exit(0)
# 24Oct2012 - temporary ^ 

# A/P Aging Summary
get_report('AP_AGING_reportListLink_Vendors', '', 10, "A/P Aging Summary", 'date_macro', 'ap_aging_summary')

# A/P Aging Detail
get_report('AP_AGING_DET_reportListLink_Vendors', '', 10, "A/P Aging Detail", 'date_macro', 'ap_aging_detail')

# Vendor Balance Summary
get_report('VEND_BAL_reportListLink_Vendors', '', 10, "Vendor Balance Summary", 'date_macro', 'vendor_bal_summary')

# Vendor Balance Detail
get_report('VEND_BAL_DET_reportListLink_Vendors', '', 10, "Vendor Balance Detail", 'date_macro', 'vendor_bal_detail')

# Unpaid Bills
get_report('UNPAID_BILLS_reportListLink_Vendors', '', 10, "Unpaid Bills", '', 'unpaid_bills')

# Expenses by Vendor Summary
get_report('VEND_EXP_reportListLink_Vendors', '', 10, "Expense by Vendor Summary", '', 'exp_by_vendor')

# Bill Payment List
get_report('BILL_PAY_LIST_reportListLink_Vendors', '', 10, "Bill Payment List", 'date_macro', 'bill_pay_list')

# Transaction List by Vendor
get_report('TX_LIST_BY_VENDOR_reportListLink_Vendors', '', 10, "Transaction List by Vendor", 'date_macro', 'txn_list_by_vendor')

# Vendor Contact List
get_report('VEND_CONTACT_reportListLink_Vendors', '', 10, "Vendor Contact List", '', "vendor_contact_list")

# Purchases by Vendor Detail
get_report('VENDOR_PURCHASE_DET_reportListLink_Vendors', '', 10, "Purchases by Vendor Detail", 'date_macro', "vendor_purchase_det")

# Purchases by Product/Service Detail
get_report('ITEM_PURCHASE_DET_reportListLink_Vendors', '', 10, "Purchases by Product/Service Detail", 'date_macro', "item_purchase_det")

# Open Purchase Order List
get_report('OPEN_PO_LIST_reportListLink_Vendors', '', 10, "Open Purchase Order List", '', "open_po_list")

# BANKING reports
# Check Detail
get_report('CHECK_DETAIL_reportListLink_Banking', '', 10, "Check Detail", 'date_macro', "check_detail")

# Reconciliation Report << SKIP for NOW? It has no Excel version
# get_report('RECONCILE_REPORTS_reportListLink_Banking', '', 10, "Reconciliation Reports", '', "reconciliation_rpts")

# Deposit Details here?

# ACCOUNTANT & TAXES report
# Trial Balance
get_report('TRIAL_BAL_reportListLink_Accountant & Taxes', '', 10, "Trial Balance", 'date_macro', "trial_balance")

# General Ledger
get_report('GEN_LEDGER_reportListLink_Accountant & Taxes', '', 10, "General Ledger", 'date_macro', "general_ledger")

# Transaction Detail by Account
get_report('TX_DET_BY_ACCT_reportListLink_Accountant & Taxes', '', 10, "Transaction Detail by Account", 'date_macro', "txn_detail_by_acct")

# Transaction List by Date
get_report('TX_LIST_BY_DATE_reportListLink_Accountant & Taxes', '', 10, "Transaction List by Date", 'date_macro', "txn_list_by_date")

# Transaction List with Splits
get_report('TX_LIST_WITH_SPLITS_reportListLink_Accountant & Taxes', '', 10, "Transaction List with Splits", 'date_macro', "txn_list_with_splits")

# Recent Transactions
get_report('RECENT_TX_reportListLink_Accountant & Taxes', '', 10, "Recent Transactions", 'moddate_macro', "recent_txn")

# PAYROLL reports not yet included
# LISTS reports
# Customer Phone List
get_report('CUST_PHONE_reportListLink_Lists', '', 10, "Customer Phone List", '', "cust_phone_list")

# Customer Contact List
get_report('CUST_CONTACT_reportListLink_Lists', '', 10, "Customer Contact List", '', "cust_contact_list")

# Vendor Phone List
get_report('VEND_PHONE_reportListLink_Lists', '', 10, "Vendor Phone List", '', "vend_phone_list")

# Vendor Contact List
get_report('VEND_CONTACT_reportListLink_Lists', '', 10, "Vendor Contact List", '', "vend_contact_list")

# Account Listing
get_report('ACCT_LIST_reportListLink_Lists', '', 10, "Account Listing", '', "acct_listing")

# Product/Service List
get_report('ITEM_PRICE_reportListLink_Lists', '', 10, "Product/Service List", '', "product_service_list")

# Payment Method Listing
get_report('PAYMENTMETHOD_LIST_reportListLink_Lists', '', 10, "Payment Method Listing", '', "pay_method_listing")

# Terms Listing
get_report('TERM_LIST_reportListLink_Lists', '', 10, "Terms Listing", '', "terms_listing")

# Recurring Template Listing
get_report('MEM_TXN_REPORT_reportListLink_Lists', '', 10, "Recurring Template Listing", '', "rcrring_templ_listing")

# proposed function
# get_report(report_link_id='ITEM_SALES_DET_reportListLink_Sales', p_send_keys='', p_seconds=5, report_name="Sales by Product/Service Detail", date_macro_name='date_macro', report_name_prefix='sales_product_service_detail')

# @TODO: find out QuickBooks' robots.txt (how to do that?) and find out what could make my scraping illegal

#driver.quit()
time.sleep(10)
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
time.sleep(10)
driver.find_element_by_link_text('Sign Out').click()
time.sleep(5)
print "Waiting for browser to close..."
logging.info("Closing browser.")
driver.quit()


# http://stackoverflow.com/questions/6363966/problem-with-iframes-in-selenium

# "Banking" link in "Reports" tab
# to access "Banking" link
# find element with id="category_BANKING"
# Deposit Detail:
# <div data_report_description="This report shows detailed information about the deposits you've made." id="DEPOSIT_DETAIL_reportListLink_Banking" class="reportListLink" data_report_token="DEPOSIT_DETAIL" data_report_url="DEPOSIT_DETAIL?" data_run_mode="launch_report">Deposit Detail</div>
# excel button:
# button_id_b5_excel_small.gif
# set firefox profile to save files automatically

# @TO-DO: get driver.page_source before AND after clicking the 'Reports' menu

# Firebug Inspect Element nav6 - Reports tab link


# 17Sep2012
#----------------------------------------------------------------
# Other reports:
# category_COMPANY 
#	>> PANDL_reportListLink_Company (Profit & Loss)
# 	>> PANDL_DET_reportListLink_Company (Profit & Loss Detail)
# 	>> BAL_SHEET_reportListLink_Company (Balance Sheet)
# 	>> BAL_SHEET_SUM_reportListLink_Company (Balance Sheet Summary)
#	>> CASH_FLOW_reportListLink_Company (Statement of Cash Flows)
#	>> ACCT_LIST_reportListLink_Company (Account Listing)
#	>> COMP_SNAPSHOT_reportListLink_Company (Company Snapshot)
#	>> SCORECARD_reportListLink_Company (Scorecard)
# Customers
#	>> AR_AGING_reportListLink_Customers (A/R Aging Summary) * has date_macro
#	>> AR_AGING_DET_reportListLink_Customers (A/R Aging Detail) * has date_macro
#	>> CUST_BAL_reportListLink_Customers (Customer Balance Summary)
#	>> CUST_BAL_DET_reportListLink_Customers (Customer Balance Detail)
#	>> COLLECTIONS_reportListLink_Customers (Collections Report)
#	>> CUST_INC_reportListLink_Customers (Income by Customer Summary)
#	>> TX_LIST_BY_CUST_reportListLink_Customers (Transaction List by Customer)
#	>> CUST_SALES_reportListLink_Customers (Sales by Customer Summary)
#	>> CUST_SALES_DET_reportListLink_Customers (Sales by Customer Detail)
#	>> INVOICE_LIST_reportListLink_Customers (Invoice List)
#	>> STATEMENT_INVOICE_reportListLink_Customers (Invoice List)
# Sales
# Skip the first 4 reports listed. They're redundant
#	>> ITEM_SALES_reportListLink_Sales (Sales by Product/Service Summary)
#	>> ITEM_SALES_DET_reportListLink_Sales (Sales by Product/Service Detail)
# Vendors
#	>> AP_AGING_reportListLink_Vendors (A/P Aging Summary)
#	>> AP_AGING_DET_reportListLink_Vendors (A/P Aging Detail)
#	>> VEND_BAL_reportListLink_Vendors (Vendor Balance Summary)
#	>> VEND_BAL_DET_reportListLink_Vendors (Vendor Balance Detail)
#	>> UNPAID_BILLS_reportListLink_Vendors (Unpaid Bills)
#	>> VEND_EXP_reportListLink_Vendors (Expense by Vendor Summary)
#	>> BILL_PAY_LIST_reportListLink_Vendors (Bill Payment List)
#	>> TX_LIST_BY_VENDOR_reportListLink_Vendors (Transaction List by Vendor)
#	reportListLink
#	>> VEND_CONTACT_reportListLink_Vendors (Vendor Contract List)
#	>> VENDOR_PURCHASE_DET_reportListLink_Vendors (Purchases by Vendor Detail)
#	>> ITEM_PURCHASE_DET_reportListLink_Vendors (Purchases by Product/Service Detail)
#	>> OPEN_PO_LIST_reportListLink_Vendors (Open Purchase Order List)
# SKIP THE FOLLOWING ENTITIES FOR NOW!
# Employees
# Payroll
# Banking
#	>> CHECK_DETAIL_reportListLink_Banking (Check Detail)
#	>> DEPOSIT_DETAIL_reportListLink_Banking (Deposit Detail) - the first report scraped
#	>> RECONCILE_REPORTS_reportListLink_Banking (Reconciliation Reports)
