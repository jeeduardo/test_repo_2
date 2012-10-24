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
    print traceback.format_exc()
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
find_click('id', 'category_BANKING', '', 2, "Getting the Banking reports")
#driver.find_element_by_id('DEPOSIT_DETAIL_reportListLink_Banking').click()
#show_loading(10, "Getting Deposit Details")
logging.info("Getting \"Deposit Details\" report...")
find_click('id', 'DEPOSIT_DETAIL_reportListLink_Banking', '', 10, "Getting \"Deposit Details\" Report")
# @TODO: set dates covered (from and to) for the report
# Deposit Detail

date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(20, "Running report") # 20 - for the meantime
driver.switch_to_default_content()
show_loading(5)
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0]) # since the page was reloaded
#time.sleep(5)
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Deposit Details\" report")
show_loading(10, "Getting Excel version of \"Deposit Details\" report")
# move file
move_report_xls("deposit_details")
time.sleep(5)

# 24Oct2012 - temporary
reload_report_list()
get_report('AP_AGING_reportListLink_Vendors', '', 10, "A/P Aging Summary", 'date_macro', 'ap_aging_summary')

# logging out
time.sleep(10)
switch_frame()
driver.find_element_by_link_text('Sign Out').click()
time.sleep(5)
driver.quit()
exit(0)
# 24Oct2012 - temporary ^ 

# 07Sep2012 - Josephson
# Go back to 'Report List' to requet for another report...
# 'Accountant and Taxes' - category_ACCOUNTANT
# The rest:
# category_COMPANY, category_CUSTOMERS, category_SALES, category_VENDORS, category_EMPLOYEES, PAYROLL, LISTS
# Journal report - JOURNAL_reportListLink_Accountant & Taxes
# 25Sep2012 - implement reload_report_list
reload_report_list()
find_click('id', 'JOURNAL_reportListLink_Accountant & Taxes', '', 10, "Getting Journal report...") # << change to &amp; ??

driver.switch_to_default_content()
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0]) # since the page was reloaded
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(20, "Running report") # 20 - for the meantime
# driver.switch_to_default_content()
driver.switch_to_default_content()
show_loading(5)

home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0]) # since the page was reloaded
#time.sleep(5)
excel_button = driver.find_element_by_id('button_id_b5_excel_small.gif')
# get report
excel_button.click()
logging.info("Getting Excel version of Journals' report...")
show_loading(10, "Getting Excel version of Journals' report...")
move_report_xls("journals")
time.sleep(5)

# 17Sep2012 - Josephson (get Profit & Loss excel report)
reload_report_list()
find_click('id', 'PANDL_reportListLink_Company', '', 10, "Getting \"Profit & Loss\" report...")
# no need for date_macro FOR NOW
show_loading(10, "Running report")
driver.switch_to_default_content()
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0]) # since the page was reloaded
show_loading(5)
excel_button = driver.find_element_by_id('button_id_b5_excel_small.gif')
excel_button.click()
logging.info("Getting Excel version of \"Profit & Loss\" report...")
show_loading(10, "Getting Excel version of \"Profit & Loss\" report...")
move_report_xls("profit_loss")
time.sleep(5)

# Profit and Loss Detail report
reload_report_list()
find_click('id', 'PANDL_DET_reportListLink_Company', '', 20, "Getting \"Profit & Loss Detail\" report...")
driver.switch_to_default_content()
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Profit & Loss Detail\" report...")
show_loading(10, "Getting Excel version of \"Profit & Loss Detail\" report...")
move_report_xls("profit_loss_detail")
time.sleep(5)


# 18Sep2012 - Balance Sheet report
#find_click('id', 'nav6', '', 10, "Getting reports")
#find_click('id', 'nav601', '', 10, "Going to 'Report List'")
#driver.switch_to_default_content()
#home_frames = driver.find_elements_by_tag_name('iframe')
#driver.switch_to_frame(home_frames[0]) # since the page was reloaded
reload_report_list()
find_click('id', 'BAL_SHEET_reportListLink_Company', '', 10, "Getting \"Balance Sheet\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Balance Sheet\" report...")
show_loading(10, "Getting Excel version of \"Balance Sheet\" report...")
move_report_xls("balance_sheet")
time.sleep(5)

#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'BAL_SHEET_SUM_reportListLink_Company', '', 10, "Getting \"Balance Sheet Summary\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Balance Sheet Summary\" report...")
show_loading(10, "Getting Excel version of \"Balance Sheet Summary\" report...")
move_report_xls("balance_sheet_summary")
time.sleep(5)

#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'CASH_FLOW_reportListLink_Company', '', 15, "Getting \"Statement of Cash Flows\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Statement of Cash Flows\"")
show_loading(10, "Getting Excel version of \"Statement of Cash Flows\"")
move_report_xls("statement_cash_flows")
time.sleep(5)

# 20Sep2012 - Account Listing report
#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'ACCT_LIST_reportListLink_Company', '', 15, "Getting \"Account Listing\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting excel version of \"Account Listing\"...")
show_loading(10, "Getting excel version of \"Account Listing\"")
move_report_xls("account_listing")
time.sleep(5)


# A/R Aging
#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'AR_AGING_reportListLink_Customers', '', 15, "Getting \"A/R Aging Summary\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(20, "Running report") # 20 - for the meantime
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting excel version of \"A/R Aging Summary\" report")
show_loading(10, "Getting excel version of \"A/R Aging Summary\" report")
move_report_xls("ar_aging_summary")
time.sleep(5)

# 27Sep2012 - A/R Aging Detail
proceed_ar_aging_detail = raw_input("proceed w/ A/R Aging Detail? (y/n)")
if (proceed_ar_aging_detail == 'y'):
  reload_report_list()
  find_click('id', 'AR_AGING_DET_reportListLink_Customers', '', 15, "Getting \"A/R Aging Detail\" report")
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  date_macro = driver.find_element_by_id('date_macro')
  date_macro.find_element_by_xpath("//option[@value='all']").click()
  driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
  show_loading(20, "Running report") # 20 - for the meantime
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  driver.find_element_by_id('button_id_b5_excel_small.gif').click()
  logging.info("Getting excel version of \"A/R Aging Detail\" report")
  show_loading(10, "Getting excel version of \"A/R Aging Detail\" report")
  move_report_xls("ar_aging_detail")
  time.sleep(3)


# Customer Balance Summary report
reload_report_list()
find_click('id', 'CUST_BAL_reportListLink_Customers', '', 15, "Getting \"Customer Balance Summary\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(20, "Running report") # 20 - for the meantime
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting excel version of \"Customer Balance Summary\" report")
show_loading(10, "Getting excel version of \"Customer Balance Summary\" report")
move_report_xls("customer_balance_summary")
time.sleep(3)


# Customer Balance Detail report
reload_report_list()
find_click('id', 'CUST_BAL_DET_reportListLink_Customers', '', 15, "Getting \"Customer Balance Detail\" report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of the \"Customer Balance Detail\" report")
show_loading(10, "Getting Excel version of the \"Customer Balance Detail\" report")
move_report_xls("customer_balance_detail")
time.sleep(3)

reload_report_list()
find_click('id', 'COLLECTIONS_reportListLink_Customers', '', 15, "Getting \"Collections\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(10, "Running report") # 10 - since Internet's faster
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Collections\" report")
show_loading(10, "Getting Excel version of \"Collections\" report")
move_report_xls("collections")
time.sleep(3)

# Income by Customer Summary
reload_report_list()
find_click('id', 'CUST_INC_reportListLink_Customers', '', 5, "Getting \"Income by Customer Summary\" report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of the \"Income by Customer Summary\" report")
show_loading(5, "Getting Excel version of the \"Income by Customer Summary\" report")
move_report_xls("income_by_customer_summary")
time.sleep(3)

# Transaction List by Customer
reload_report_list()
find_click('id', 'TX_LIST_BY_CUST_reportListLink_Customers', '', 5, "Getting \"Transaction List by Customer\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(5, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Transaction List by Customer\" report")
show_loading(10, "Getting Excel version of \"Transaction List by Customer\" report")
move_report_xls("txn_list_by_customer")
time.sleep(3)

# Sales by Customer Summary
reload_report_list()
find_click('id', 'CUST_SALES_reportListLink_Customers', '', 5, "Getting \"Sales by Customer Summary\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(5, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Sales by Customer Summary\" report")
show_loading(5, "Getting Excel version of \"Sales by Customer Summary\" report")
move_report_xls("sales_by_customer_summary")
time.sleep(3)

# Sales by Customer Detail
reload_report_list()
find_click('id', 'CUST_SALES_DET_reportListLink_Customers', '', 5, "Getting \"Sales by Customer Detail\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(5, "Running report") # 20 - for the meantime
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Sales by Customer Detail\" report")
show_loading(5, "Getting Excel version of \"Sales by Customer Detail\" report")
move_report_xls("sales_by_customer_detail")
time.sleep(3)

# Invoice List
reload_report_list()
find_click('id', 'INVOICE_LIST_reportListLink_Customers', '', 5, "Getting \"Invoice List\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(5, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Invoice List\" report")
show_loading(10, "Getting Excel version of \"Invoice List\" report")
move_report_xls("invoice_list")
time.sleep(3)

# Statement List
reload_report_list()
find_click('id', 'STATEMENT_INVOICE_reportListLink_Customers', '', 5, "Getting \"Statement List\" report")
switch_frame()
date_macro = driver.find_element_by_id('stmtdate_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(5, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Statement List\" report")
show_loading(10, "Getting Excel version of \"Statement List\" report")
move_report_xls("statement_list")
time.sleep(3)

# Sales by Product/Service Summary
reload_report_list()
find_click('id', 'ITEM_SALES_reportListLink_Sales', '', 5, "Getting \"Sales by Product/Service Summary\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(10, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Sales by Product/Service Summary\" report")
show_loading(5, "Getting Excel version of \"Sales by Product/Service Summary\" report")
# move file
move_report_xls("sales_product_service_summary")
time.sleep(3)

# Sales by Product/Service Detail
reload_report_list()
find_click('id', 'ITEM_SALES_DET_reportListLink_Sales', '', 5, "Getting \"Sales by Product/Service Detail\" report")
switch_frame()
date_macro = driver.find_element_by_id('date_macro')
date_macro.find_element_by_xpath("//option[@value='all']").click()
driver.find_element_by_id('button_id_b5_run_report_small.gif').click()
show_loading(10, "Running report")
switch_frame()
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
logging.info("Getting Excel version of \"Sales by Product/Service Detail\" report")
show_loading(5, "Getting Excel version of \"Sales by Product/Service Detail\" report")
# move file
move_report_xls("sales_product_service_detail")
time.sleep(3)
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
driver.quit()
exit()


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
