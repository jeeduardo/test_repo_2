#!/usr/bin/python
from selenium import webdriver
from datetime import datetime
import time
import os
import re
import ConfigParser
import logging
import platform

import sys
sys.path.append(os.getcwd() + '/../utils')
import enc_pwd
import sendmail

# setup spr_client
import gdata.spreadsheet
import gdata.spreadsheet.text_db
import gdata.auth

# setup time the backup has started
dd_ba_start = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

# setup logging
print "Setting up logging..."
logging.basicConfig(filename='quickbooks-report-dump.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

# get configurations
cfg_file = 'quickbooks-report-dump.cfg'
cfg = ConfigParser.ConfigParser()
cfg.read(cfg_file)

# move the credentials to config
spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = cfg.get('gdata_credentials', 'gdata_username')
spr_client.password = enc_pwd.decrypt_pword(cfg.get('gdata_credentials', 'gdata_pword'), os.getcwd()+os.sep)
logging.info("Logging in to google spreadsheet app.")

spr_client.ProgrammaticLogin()

spreadsheet_key = cfg.get('gdata_credentials', 'spreadsheet_key')
# default
wfeed = spr_client.GetWorksheetsFeed(key=spreadsheet_key)
for wksht in wfeed.entry:
  wksht_id = wksht.id.text.split('/')[-1]

feed = spr_client.GetListFeed(spreadsheet_key, wksht_id)
hdr_record = gdata.spreadsheet.text_db.Record(row_entry=feed.entry[0])
offset = 1 + len(hdr_record.content)

# function to send email
def send_mail(subject, msg):
  print "Sending email..."
  logging.info("sending email with subject %s..." %(subject))
  sendmail.email(os.getcwd()+os.sep+'quickbooks-report-dump.cfg', subject, msg)

# print dots . . .  to screen with given no. of seconds
def show_loading(p_seconds = 60, p_msg_while_waiting=''):
  print p_msg_while_waiting
  loading_cmd = ''
  for i in range(1, p_seconds+1):
    loading_cmd = loading_cmd + "echo -n '.'; sleep 1; "
  os.system(loading_cmd)
  print

# clicks a web element
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
    tb = traceback.format_exc()
    logging.error(tb)
    error_email_msg = "The following error was encountered while the script was running:\n %s" %(tb)
    print error_email_msg
    send_mail("QuickBooks: Error in report scraping", error_email_msg)
    # exit()

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
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])

send_mail("QuickBooks report dump has started", "The QuickBooks report dump script has started. We shall email you again for details.")

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
ppword = enc_pwd.decrypt_pword(cfg.get('credentials', 'ppword'), os.getcwd() + os.sep)

download_dir = cfg.get('prefs', 'download_dir')
save_to_disk = cfg.get('prefs', 'save_to_disk_immed')
#24Oct2012 - dirname
dirname = cfg.get('prefs', 'dirname')

# 24Sep2012 - get command named used to move/rename file(s) and DIRECTORY separator
# move - for windows
# mv - for linux/unix
mv = cfg.get('prefs', 'move_command')
sep = os.sep

# create download directory
datetime_now = datetime.now()
download_dir_full_path = download_dir + sep + dirname + datetime_now.strftime('%Y-%m-%d_%H%M')

# move file to target directory
def move_report_xls(report_name_prefix):
  global mv, download_dir_download_dir_full_path, datetime_now
  mv_cmd = "%s -v $(ls -t %s/report*.xls | head -n1) %s/%s_%s.xls" %(mv, download_dir, download_dir_full_path, report_name_prefix, datetime_now.strftime('%Y-%m-%d_%H%M'))
  logging.info(mv_cmd)
  return os.system(mv_cmd)

logging.info("creating download directory %s" %(download_dir_full_path))
os.system("mkdir %s" %(download_dir_full_path))

# get report - D.R.Y
# deprecate p_send_keys and pass '' instead on find_click?
#def get_report(report_link_id, p_send_keys, p_seconds, report_name, date_macro_name, report_name_prefix):
def get_report(report_link_id, p_seconds, report_name, date_macro_name, report_name_prefix):
  global driver, row_no
  try:
    print "Getting report named \"%s\"" %(report_name)
    reload_report_list()
    # 13Dec2012 - initialize p_send_keys to blank
    p_send_keys = ''
    find_click('id', report_link_id, p_send_keys, p_seconds, "Getting \"%s\" report" %(report_name))
    switch_frame()
    if (date_macro_name <> ""):
      date_macro = driver.find_element_by_id(date_macro_name)
      date_macro.find_element_by_xpath("//option[@value='all']").click()
      driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
      # 21Jan2013 - change from 10 to p_seconds
      show_loading(p_seconds, "Running report")
      switch_frame()

    driver.find_element_by_id('button_id_b5_excel_small.gif').click()
    logging.info("Getting Excel version of \"%s\" report" %(report_name))

    show_loading(5, "Getting Excel version of \"%s\" report" %(report_name))
    # move file
    move_report_xls(report_name_prefix)
    logging.info("Updating accounting sheet for %s report." %(report_name))
    update_acct_cell(row_no, "OK", report_link_id, report_name)
    row_no += 1
    time.sleep(3)
  except:
#    import traceback
#    tb = traceback.format_exc()
#    logging.error(tb)
#    err_email_msg = "Hi,\n\n\
#Something went wrong with extracting a report of %s. Please check. \
#Below are the error details:\n\n%s" %(report_name, tb)
#    send_mail("QuickBooks: ERROR in extracting reports", err_email_msg)
    update_acct_cell(row_no, "ERROR. See email for details", report_link_id, report_name)
    row_no += 1
    time.sleep(3)
    raise Exception("Something went wrong in scraping the reports.")
  return 0

# 08Nov2012 - get payroll reports
def get_payroll_report(payroll_report_url, caption, file_prefix):
  global mv, download_dir, download_dir_full_path, datetime_now, row_no
  try:
    print "Getting report for \"%s\" summary" %(caption)
    logging.info("Getting report for \"%s\" in %s" %(caption, payroll_report_url))
    driver.get(payroll_report_url)
    # 29Dec2012 - dummy error
    show_loading(10)
    p = os.popen("ls -t %s/*.xls | head -n1" %(download_dir))
    fr = re.escape(p.readline().strip())
    # move file to download_dir_full_path
    mv_cmd = "%s -v %s %s/%s_%s.xls" %(mv, fr, download_dir_full_path, file_prefix, datetime_now.strftime('%Y-%m-%d_%H%M'))
    p.close()
    logging.info(mv_cmd)
    print mv_cmd
    os.system(mv_cmd)
    logging.info("Updating accounting sheet for %s report" % (caption))
    update_acct_cell(row_no, "OK", "", caption)
    row_no += 1
  except:
    import traceback
    tb = traceback.format_exc()
    logging.error("ERROR occured on Quickbooks report dump:\n")
    logging.error(tb)
    print tb
    err_email_msg = "ERROR occured on Quickbooks report dump:\n%s" %(tb)
    send_mail("Error on Quickbooks report dump.", err_email_msg)
    raise Exception("Error on QuickBooks report dump.")

  return 0


def update_acct_cell(row_no, status, report_link_id, report_name):
  global spr_client, offset, wksht_id
  spreadsheet_id = '0AjKELoU3HY0HdEx4MzR1eE1aWUFaem1QZ2VUc0NlVVE'
  # wksht_id = 'od7'

  # 27Dec2012 - 2 lines below are temporary
  print "Updating worksheet id %s" %(wksht_id)

  if (datetime.now().day == 1):
    spr_client.UpdateCell(row_no, 1, report_link_id, spreadsheet_id, wksht_id)
    spr_client.UpdateCell(row_no, 2, report_name, spreadsheet_id, wksht_id)

  return spr_client.UpdateCell(row_no, offset, status, spreadsheet_id, wksht_id)


# set Firefox profile
logging.info("Loading Firefox profile...")
fp = webdriver.FirefoxProfile()
#fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting", False) # False
fp.set_preference("browser.download.dir", download_dir)#"C:\Users\josephson\Downloads")
#fp.set_preference("browser.download.dir", os.getcwd())
# 03Sept2012 - Josephson (file type="application/vnd.ms-excel")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", save_to_disk) #"application/vnd.ms-excel")

try:
  driver = webdriver.Firefox(firefox_profile=fp)
except:
  import traceback
  tb = traceback.format_exc()
  print tb
  logging.error(tb)
  exit(1)
driver.get(url)
logging.info("Loading QuickBooks")
logging.info("Loading %s" %(url))
show_loading(10, "Loading %s" % (url))
#/home/ubuntu/qboe/test_repo_2/quickbooks

logging.info("Logging in as %s" % (username))
# 04Sep2012 - Josephson (testing the _find_it function)
find_click('name', 'login', username, 2)

find_click('name', 'password', ppword, 2)
# login_wait_time - set time (in seconds) to wait for loading the home page completely
login_wait_time = int(cfg.get('prefs', 'login_wait_time'))
find_click('id', 'LoginButton', '', login_wait_time, "Logging in and loading home page. ")


# go to first frame, click the 'Reports' tab
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0])
show_loading(10)


# 09Nov20012 - get cookies; to be deleted later for logout
cookies = driver.get_cookies()
show_loading(3)
# 09Nov20012
find_click('id', 'nav6', '', 10, "Getting reports")

# the 'Report List' submenu
# driver.find_element_by_id('nav601').click()
find_click('id', 'nav601', '', 10, "Going to 'Report List'")


logging.info("Getting the Banking reports")

# use get_report instead
# Deposit Details
# EXCEPTION handling test - 10Dec2012
try:
  # add new sheet if it's the beginning of month
  if (datetime.now().day == 1):
    spr_client.AddWorksheet(datetime_now.strftime('%m-%Y'), 64, 34, spreadsheet_key)
    wfeed = spr_client.GetWorksheetsFeed(key=spreadsheet_key)
    for wksht in wfeed.entry:
      wksht_id = wksht.id.text.split('/')[-1]

    offset = 4
    spr_client.UpdateCell(2, 1, "Report Id", spreadsheet_key, wksht_id)
    spr_client.UpdateCell(2, 2, "Report", spreadsheet_key, wksht_id)
    spr_client.UpdateCell(2, 3, "Remarks", spreadsheet_key, wksht_id)

  spr_client.UpdateCell(2, offset, datetime_now.strftime('%Y-%m-%d'), spreadsheet_key, wksht_id)
  row_no = 3

  # 22Jan2013 - report_wait_time - to replace 2nd parameter with this
  report_wait_time = int(cfg.get('prefs', 'report_wait_time'))

  get_report('DEPOSIT_DETAIL_reportListLink_Banking', report_wait_time, "Deposit Details", 'date_macro', "deposit_details") 
  
  # find_click('id', 'category_BANKING', '', 2, "Getting the Banking reports")
  reload_report_list()
  
  # Journal
  get_report('JOURNAL_reportListLink_Accountant &amp; Taxes', report_wait_time, "Journal", 'date_macro', "journals")
  
  # Profit & Loss
  # 21Jan2013 - in an attempt to simulate an error, i'd change 10 seconds (parameter 2) to 1
  get_report('PANDL_reportListLink_Company', report_wait_time, "Profit & Loss", '', "profit_loss")
  
  # Profit & Loss Detail
  get_report('PANDL_DET_reportListLink_Company', report_wait_time, "Profit & Loss Detail", '', "profit_loss_detail")
  
  # Balance Sheet
  get_report('BAL_SHEET_reportListLink_Company', report_wait_time, "Balance Sheet", '', "balance_sheet")
  
  # Balance Sheet Summary
  get_report('BAL_SHEET_SUM_reportListLink_Company', report_wait_time, "Balance Sheet Summary", '', "balance_sheet_summary")
  
  # Statement of Cash Flows
  # 17Dec2012 - TEST ERROR here!
  get_report('CASH_FLOW_reportListLink_Company', report_wait_time, "Statement of Cash Flows", '', "statement_cash_flows")
  
  # A/R Aging
  get_report('AR_AGING_reportListLink_Customers', report_wait_time, "A/R Aging Summary", 'date_macro', "ar_aging_summary")
  
  # A/R Aging Detail
  get_report('AR_AGING_DET_reportListLink_Customers', report_wait_time, "A/R Aging Detail", 'date_macro', "ar_aging_detail")
  
  # Customer Balance Summary
  get_report('CUST_BAL_reportListLink_Customers', report_wait_time, "Customer Balance Summary", 'date_macro', "customer_balance_summary")
  
  # Customer Balance Detail
  get_report('CUST_BAL_DET_reportListLink_Customers', report_wait_time, "Customer Balance Detail", '', "customer_balance_detail")
  
  # Collections
  get_report('COLLECTIONS_reportListLink_Customers', report_wait_time, "Collections", 'date_macro', "collections")
  
  # Income by Customer Summary
  get_report('CUST_INC_reportListLink_Customers', report_wait_time, "Income by Customer Summary", '', "income_by_cust_summary")
  
  # Transaction List by Customer
  get_report('TX_LIST_BY_CUST_reportListLink_Customers', report_wait_time, "Transaction List by Customer", 'date_macro', "txn_list_by_customer")
  
  # Sales by Customer Summary
  get_report('CUST_SALES_reportListLink_Customers', report_wait_time, "Sales by Customer Summary", 'date_macro', "sales_by_customer_summary")
  
  # Sales by Customer Detail
  get_report('CUST_SALES_DET_reportListLink_Customers', report_wait_time, "Sales by Customer Detail", 'date_macro', "sales_by_customer_detail")
  
  # Invoice List
  get_report('INVOICE_LIST_reportListLink_Customers', report_wait_time, "Invoice List", 'date_macro', "invoice_list")
  
  # Statement List
  get_report('STATEMENT_INVOICE_reportListLink_Customers', report_wait_time, "Statement List", 'stmtdate_macro', "statement_list")
  
  # Sales by Product/Service Summary
  get_report('ITEM_SALES_reportListLink_Sales', report_wait_time, "Sales by Product/Service Summary", 'date_macro', "sales_product_service_summary")
  
  # Sales by Product/Service Detail
  get_report('ITEM_SALES_DET_reportListLink_Sales', report_wait_time, "Sales by Product/Service Detail", 'date_macro', "sales_product_service_detail")
  
  # A/P Aging Summary
  get_report('AP_AGING_reportListLink_Vendors', report_wait_time, "A/P Aging Summary", 'date_macro', 'ap_aging_summary')
  
  # A/P Aging Detail
  get_report('AP_AGING_DET_reportListLink_Vendors', report_wait_time, "A/P Aging Detail", 'date_macro', 'ap_aging_detail')
  
  # Vendor Balance Summary
  get_report('VEND_BAL_reportListLink_Vendors', report_wait_time, "Vendor Balance Summary", 'date_macro', 'vendor_bal_summary')
  
  # Vendor Balance Detail
  get_report('VEND_BAL_DET_reportListLink_Vendors', report_wait_time, "Vendor Balance Detail", 'date_macro', 'vendor_bal_detail')
  
  # Unpaid Bills
  get_report('UNPAID_BILLS_reportListLink_Vendors', report_wait_time, "Unpaid Bills", '', 'unpaid_bills')
  
  # Expenses by Vendor Summary
  get_report('VEND_EXP_reportListLink_Vendors', report_wait_time, "Expense by Vendor Summary", '', 'exp_by_vendor')
  
  # Bill Payment List
  get_report('BILL_PAY_LIST_reportListLink_Vendors', report_wait_time, "Bill Payment List", 'date_macro', 'bill_pay_list')
  
  # Transaction List by Vendor
  get_report('TX_LIST_BY_VENDOR_reportListLink_Vendors', report_wait_time, "Transaction List by Vendor", 'date_macro', 'txn_list_by_vendor')
  
  # Vendor Contact List
  get_report('VEND_CONTACT_reportListLink_Vendors', report_wait_time, "Vendor Contact List", '', "vendor_contact_list")
  
  # Purchases by Vendor Detail
  get_report('VENDOR_PURCHASE_DET_reportListLink_Vendors', report_wait_time, "Purchases by Vendor Detail", 'date_macro', "vendor_purchase_det")
  
  # Purchases by Product/Service Detail
  get_report('ITEM_PURCHASE_DET_reportListLink_Vendors', report_wait_time, "Purchases by Product/Service Detail", 'date_macro', "item_purchase_det")
  
  # Open Purchase Order List
  get_report('OPEN_PO_LIST_reportListLink_Vendors', report_wait_time, "Open Purchase Order List", '', "open_po_list")
  
  # BANKING reports
  # Check Detail
  get_report('CHECK_DETAIL_reportListLink_Banking', report_wait_time, "Check Detail", 'date_macro', "check_detail")
  
  # Reconciliation Report << SKIP for NOW? It has no Excel version
  # get_report('RECONCILE_REPORTS_reportListLink_Banking', '', report_wait_time, "Reconciliation Reports", '', "reconciliation_rpts")
  
  # Deposit Details here?
  
  # ACCOUNTANT & TAXES report
  # Trial Balance
  get_report('TRIAL_BAL_reportListLink_Accountant &amp; Taxes', report_wait_time, "Trial Balance", 'date_macro', "trial_balance")
  
  # General Ledger
  get_report('GEN_LEDGER_reportListLink_Accountant &amp; Taxes', report_wait_time, "General Ledger", 'date_macro', "general_ledger")
  
  # Transaction Detail by Account
  get_report('TX_DET_BY_ACCT_reportListLink_Accountant &amp; Taxes', report_wait_time, "Transaction Detail by Account", 'date_macro', "txn_detail_by_acct")
  
  # Transaction List by Date
  get_report('TX_LIST_BY_DATE_reportListLink_Accountant &amp; Taxes', report_wait_time, "Transaction List by Date", 'date_macro', "txn_list_by_date")
  
  # Transaction List with Splits
  get_report('TX_LIST_WITH_SPLITS_reportListLink_Accountant &amp; Taxes', report_wait_time, "Transaction List with Splits", 'date_macro', "txn_list_with_splits")
  
  # Recent Transactions
  get_report('RECENT_TX_reportListLink_Accountant &amp; Taxes', report_wait_time, "Recent Transactions", 'moddate_macro', "recent_txn")
  
  # PAYROLL reports not yet included
  # LISTS reports
  # Customer Phone List
  get_report('CUST_PHONE_reportListLink_Lists', report_wait_time, "Customer Phone List", '', "cust_phone_list")
  
  # Customer Contact List
  get_report('CUST_CONTACT_reportListLink_Lists', report_wait_time, "Customer Contact List", '', "cust_contact_list")
  
  # Vendor Phone List
  get_report('VEND_PHONE_reportListLink_Lists', report_wait_time, "Vendor Phone List", '', "vend_phone_list")
  
  # Vendor Contact List
  get_report('VEND_CONTACT_reportListLink_Lists', report_wait_time, "Vendor Contact List", '', "vend_contact_list")
  
  # Account Listing
  get_report('ACCT_LIST_reportListLink_Lists', report_wait_time, "Account Listing", '', "acct_listing")
  
  # Product/Service List
  get_report('ITEM_PRICE_reportListLink_Lists', report_wait_time, "Product/Service List", '', "product_service_list")
  
  # Payment Method Listing
  get_report('PAYMENTMETHOD_LIST_reportListLink_Lists', report_wait_time, "Payment Method Listing", '', "pay_method_listing")
  
  # Terms Listing
  get_report('TERM_LIST_reportListLink_Lists', report_wait_time, "Terms Listing", '', "terms_listing")
  
  # Recurring Template Listing
  get_report('MEM_TXN_REPORT_reportListLink_Lists', report_wait_time, "Recurring Template Listing", '', "recrring_templ_listing")
except:
  import traceback
  tb = traceback.format_exc()
  print tb
  logging.error(tb)
  print "Program's exiting. Please see email for details."
  logging.error("Program's exiting. Please see email for details")
  exit(1)
# EXCEPTION handling test - 10Dec2012

# proposed function
# get_report(report_link_id='ITEM_SALES_DET_reportListLink_Sales', p_send_keys='', p_seconds=5, report_name="Sales by Product/Service Detail", date_macro_name='date_macro', report_name_prefix='sales_product_service_detail')


# 09Nov2012
# TO-DO: downloading reports based from a google spreadsheet
# TO-DO: accounting of payroll reports
try:
  reload_report_list()
  year_str = str(datetime_now.year)

  # Payroll Summary
  payroll_summary_url = cfg.get('payroll_reports_url', 'payroll_summary_url') %("01/01/"+year_str, "12/31/"+year_str)
  get_payroll_report(payroll_summary_url, "Payroll Summary", "Payroll_Summary")

  # Payroll Details
  payroll_details_url = cfg.get('payroll_reports_url', 'payroll_details_url') %(year_str, year_str)
  get_payroll_report(payroll_details_url, "Payroll Details", "Payroll_Details")

  # Payroll Deductions/Contributions
  deducts_contribs_url = cfg.get('payroll_reports_url', 'deducts_contribs_url') %(year_str, year_str)
  get_payroll_report(deducts_contribs_url, "Payroll Deductions/Contributions", "Deductions_Contributions")

  # Skipping "Last Paycheck" report (because it appears to only print rhe most recent paycheck - as the report name implies
  # Employee Details
  employee_details_url = cfg.get('payroll_reports_url', 'employee_details_url') %(year_str, datetime_now.strftime("%m/%d/%Y"))
  get_payroll_report(employee_details_url, "Employee Details", "Employee_Details")
  
  # Tax Liability
  tax_liability_url = cfg.get('payroll_reports_url', 'tax_liability_url') %(year_str, year_str)
  get_payroll_report(tax_liability_url, "Tax Liability", "Tax_Liability")

  # Payroll Tax and Wage Summary
  tax_wage_summary_url = cfg.get('payroll_reports_url', 'tax_wage_summary_url') %(year_str, year_str)
  get_payroll_report(tax_wage_summary_url, "Payroll Tax and Wage Summary", "Tax_Wage_Summary")

  # Total Pay
  total_pay_url = cfg.get('payroll_reports_url', 'total_pay_url') %(year_str, year_str)
  get_payroll_report(total_pay_url, "Total Pay", "Total_Pay")

  # Payroll Tax Payments
  tax_payments_url = cfg.get('payroll_reports_url', 'tax_payments_url') %(year_str, year_str)
  get_payroll_report(tax_payments_url, "Payroll Tax Payments", "Tax_Payments")

  # Workers' Compensation
  workers_comp_url = cfg.get('payroll_reports_url', 'workers_comp_url') %(year_str, year_str)
  get_payroll_report(workers_comp_url, "Workers' Compensation", "Workers_Compensation")

  # Vacation and Sick Leave
  vl_sl_url = cfg.get('payroll_reports_url', 'vl_sl_url') %(year_str, year_str)
  get_payroll_report(vl_sl_url, "Vacation and Sick Leave", "Vacation_Sick_Leave")

  # Billing Summary
  billing_summary_url = cfg.get('payroll_reports_url', 'billing_summary_url') %(year_str, year_str)
  get_payroll_report(billing_summary_url, "Billing Summary", "Billing_Summary")

  # Total Cost
  total_cost_url = cfg.get('payroll_reports_url', 'total_cost_url') %(year_str, year_str)
  get_payroll_report(total_cost_url, "Total Cost", "Total_Cost")

  # Retirement Plans
  retirement_plans_url = cfg.get('payroll_reports_url', 'retirement_plans_url') %(year_str, year_str)
  get_payroll_report(retirement_plans_url, "Retirement Plans", "Retirement_Plans")
  print "Deleting cookies..."
  for i in range(0, len(cookies)):
    driver.delete_cookie(cookies[i]['name'])

except:

  import traceback
  tb = traceback.format_exc()
  logging.error(tb)
  print tb
  html_file = open('html_' + datetime_now.strftime('%Y-%m-%d_%H%M%S'), 'w')
  html_file.write(driver.page_source.encode('ascii', 'ignore'))
  html_file.close()
  # TO-DO: send ERROR email if something wrong happens
  # send error email

  err_email_msg = "Hi,\n\nThere has been an error while scraping for the QuickBooks reports.\nPlease see below stack trace for details:\n\n%s" %(tb)
  send_mail("ERROR in QuickBooks Report Dump automation.", err_email_msg)

  exit(1)

show_loading(5)
print "Waiting for browser to close..."
logging.info("Closing browser.")
# TO-DO: send email
# logging.info("python %s/../utils/sendmail.py --cfg %s --subject \"QuickBooks Report Dump has finished.\" --message \"Please check folder %s for the report files.\"" %(os.getcwd(), os.getcwd()+os.sep+'quickbooks-report-dump.cfg', download_dir_full_path))
# os.system("python %s/../utils/sendmail.py --cfg %s --subject \"QuickBooks Report Dump has finished.\" --message \"Please check folder %s for the report files.\"" %(os.getcwd(), os.getcwd()+os.sep+'quickbooks-report-dump.cfg', download_dir_full_path))
send_mail("QuickBooks Report Dump has finished.", "Please check folder %s for the report files." %(download_dir_full_path))
# 21Jan2013 temporary
# calculate dump size
# download directory BA accounting
dd_ba_dict = {'date':datetime_now.strftime("%m/%d/%Y"), 'directoryname':os.path.split(download_dir_full_path)[1],'error':'None'}

total_dump_size = 0L
for dirpath, dirnames, filenames in os.walk(download_dir_full_path):
  for f in filenames:
    fp = os.path.join(dirpath, f)
    total_dump_size += os.path.getsize(fp)

# print "total_dump_size =", str(float(total_dump_size))
total_dump_size_kb = float(total_dump_size)/1024.0
dd_ba_dict['size'] =  "%.2f KB" %(total_dump_size_kb)
dd_ba_dict['start'] = dd_ba_start
dd_ba_dict['end'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
dd_ba_key = '0AjKELoU3HY0HdGw2MlFSN01lelRDd3I4bVJ6czJSSnc'
spr_client.InsertRow(dd_ba_dict, dd_ba_key, 'od6')
# 21Jan2013
show_loading(10)
driver.quit()




# 12Nov2012 - removing some notes
# 17Sep2012
#----------------------------------------------------------------
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
# Payroll

