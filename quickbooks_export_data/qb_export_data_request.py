#!/usr/bin/python
import logging
import time
import os
from selenium import webdriver
from datetime import datetime, timedelta
from re import search
from ConfigParser import ConfigParser

cfg = ConfigParser()
cfg.read('qb_export_data.cfg')

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
# 03/15/2013
##pword = cfg.get('credentials', 'pword')
cmd_str = "./../utils/encpwd/read_cfg_pwd.sh ../../quickbooks_export_data/qb_export_data.cfg credentials pword"
pword = os.popen(cmd_str).readline().strip()
email_address = cfg.get('email_credentials', 'username')
export_data_request_url = cfg.get('other_settings', 'export_data_request_url') + ("&user_email=%s&user_name=%s" %(email_address, username))

# setup logging
log_filename=os.getcwd() + os.sep + cfg.get('other_settings', 'log_file')
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

# check if export request has been made already
datetime_now = datetime.now()
datetime_pdt = datetime_now - timedelta(hours=7)
# date_today = datetime_now.strftime('%Y%m%d')
# search for PDT date in log file
# 03/15/2013 - might still return 0 even if there are no results found
# grep_cmd = "grep -q \"REQUEST FOR TODAY, %s, WRITTEN TO LOG FILE\!\" %s" %(datetime_pdt.strftime('%Y-%m-%d'), log_filename)
grep_cmd = "grep \"REQUEST FOR TODAY, %s, WRITTEN TO LOG FILE\!\" %s | wc -l" %(datetime_pdt.strftime('%Y-%m-%d'), log_filename)
try:
  # grep_rs = os.system(grep_cmd)
  grep_rs = os.popen(grep_cmd).readline().strip()
except:
  import traceback
  print "An error was encountered. Please check %s for details." %(log_filename)
  logging.error(traceback.format_exc())
finally:
  ### if (grep_rs == 0):
  if (grep_rs <> '0'):
    print "REQUESTED"
    logging.info("Request has been made already. Please wait for the email to be delivered.")
    exit(0)
  else:
    print "REQUESTING"
    logging.info("Proceeding in requesting for data export.")

logging.info("Opening firefox...")

try:
  driver = webdriver.Firefox()

  driver.get(url)
  login = driver.find_element_by_name('login')
  login.click()
  # login.clear()
  login.send_keys(username)
  ppword = driver.find_element_by_name('password')
  ppword.click()
  # ppword.clear()
  ppword.send_keys(pword)
  time.sleep(2)
  logging.info("Logging in as %s" %(username))
  driver.find_element_by_id('LoginButton').click()
  
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  
  # print "export_data_request_url: %s" %export_data_request_url
  logging.info("Requesting data...")
  time.sleep(10)
  driver.get(export_data_request_url)
  
  time.sleep(60)
  # write the timestamp for the request (to make sure that the request made for the day will not be forgotten)
  # 25Oct2012 - write to log file
  #outfile = open('qb_export_data_request_time', 'w')
  #outfile.write(date_today)
  #outfile.close()
  logging.info("Request for today has been recorded.")
  logging.info("REQUEST FOR TODAY, %s, WRITTEN TO LOG FILE!" %(datetime_pdt.strftime('%Y-%m-%d')))
  
  driver.get(url)
  time.sleep(30)
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  time.sleep(2)
  logging.info("Signing out")
  driver.find_element_by_link_text('Sign Out').click()
  time.sleep(10)
  driver.quit()
except:
  import traceback
  tb = traceback.format_exc()
  print "-----THERE WAS AN ERROR-----"
  print tb
  logging.error(tb)
  exit(1)
finally:
  exit(0)
