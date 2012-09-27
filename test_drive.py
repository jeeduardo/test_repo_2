#!/usr/bin/python
from selenium import webdriver
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
  for i in range(1, p_seconds+1):
    print '.',
    time.sleep(1)
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
  except Exception, e:
    print 'ERROR:', e
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

# 05Sep2012 - enable logging
# 25Sep2012 - use os.sep for directory separator
logging.basicConfig(filename=os.getcwd() + os.sep + 'quickbooks_dump.log', level=logging.INFO, format='%(asctime) %(levelname)s : %(message)s')

# 04Sep2012 - get configurations
cfg = ConfigParser.ConfigParser()
cfg.read('dump_casc_qboe_other.cfg')

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

# 24Sep2012 - get command named used to move/rename file(s) and DIRECTORY separator
# move - for windows
# mv - for linux/unix
mv = cfg.get('prefs', 'move_command')
sep = os.sep

print mv

# ec2-107-22-54-11.compute-1.amazonaws.com *YHyttwQNuz

# set Firefox profile
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
show_loading(10, "Loading %s" % (url))

# 04Sep2012 - Josephson (testing the _find_it function)
find_click('name', 'login', username, 2)

find_click('name', 'password', ppword, 2)
#driver.find_element_by_id('LoginButton').click()
find_click('id', 'LoginButton', '', 60, "Logging in and loading home page. ")


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
find_click('id', 'category_BANKING', '', 2, "Getting the Banking reports")
#driver.find_element_by_id('DEPOSIT_DETAIL_reportListLink_Banking').click()
#show_loading(10, "Getting Deposit Details")
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
show_loading(10, "Getting Excel version of report")

# 07Sep2012 - Josephson
# Go back to 'Report List' to requet for another report...
# 'Accountant and Taxes' - category_ACCOUNTANT
# The rest:
# category_COMPANY, category_CUSTOMERS, category_SALES, category_VENDORS, category_EMPLOYEES, PAYROLL, LISTS
# Journal report - JOURNAL_reportListLink_Accountant & Taxes
# 25Sep2012 - implement reload_report_list
reload_report_list()
# 10Sep2012 - Josephson (other reports)

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
show_loading(10, "Getting Excel version of Journals' report...")

# 17Sep2012 - Josephson (get Profit & Loss excel report)
#find_click('id', 'nav6', '', 10, "Getting reports")
#find_click('id', 'nav601', '', 10, "Going to 'Report List'")
#driver.switch_to_default_content()
#home_frames = driver.find_elements_by_tag_name('iframe')
#driver.switch_to_frame(home_frames[0]) # since the page was reloaded
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
show_loading(10, "Getting Excel version of \"Profit & Loss\" report...")

# Profit and Loss Detail report
#find_click('id', 'nav6', '', 10, "Getting reports")
#find_click('id', 'nav601', '', 10, "Going to 'Report List'")
#driver.switch_to_default_content()
#home_frames = driver.find_elements_by_tag_name('iframe')
#driver.switch_to_frame(home_frames[0]) # since the page was reloaded
reload_report_list()
find_click('id', 'PANDL_DET_reportListLink_Company', '', 20, "Getting \"Profit & Loss Detail\" report...")
driver.switch_to_default_content()
home_frames = driver.find_elements_by_tag_name('iframe')
driver.switch_to_frame(home_frames[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
show_loading(10, "Getting Excel version of \"Profit & Loss Detail\" report...")


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
show_loading(10, "Getting Excel version of \"Balance Sheet\" report...")

#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'BAL_SHEET_SUM_reportListLink_Company', '', 10, "Getting \"Balance Sheet Summary\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
show_loading(10, "Getting Excel version of \"Balance Sheet Summary\" report...")

#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'CASH_FLOW_reportListLink_Company', '', 15, "Getting \"Statement of Cash Flows\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
show_loading(10, "Getting Excel version of \"Statement of Cash Flows\"")

# 20Sep2012 - Account Listing report
#find_click('id', 'nav6', '', 10)
reload_report_list()
find_click('id', 'ACCT_LIST_reportListLink_Company', '', 15, "Getting \"Account Listing\" report")
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
driver.find_element_by_id('button_id_b5_excel_small.gif').click()
show_loading(10, "Getting excel version of \"Account Listing\"")


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
show_loading(10, "Getting excel version of \"A/R Aging Summary\" report")

# 27Sep2012
reload_report_list()

# try the interactive python shell IF things go wrong...

# 03Sept2012 - Josephson (don't sign it out just yet!)
#print 'Testing Sign Out...'
#driver.find_element_by_partial_link_text('Sign Out').click()
#
#time.sleep(10)

# @TODO: find out QuickBooks' robots.txt (how to do that?) and find out what could make my scraping illegal

#driver.quit()
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

# @TO-DO: run this on a linux box with a READ desktop - NOT Xvfb!


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
# REMEMBER to 'rename' the downloaded XLS files.. Don't just let them be named report1.xls, report.2.xls , etc. 
# as this is not helpful in describing the report...
