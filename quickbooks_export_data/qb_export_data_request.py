#!/usr/bin/python
import logging
import time
import os
from selenium import webdriver
from datetime import datetime
from re import search
from ConfigParser import ConfigParser

cfg = ConfigParser()
cfg.read('qb_export_data.cfg')

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
pword = cfg.get('credentials', 'pword')
email_address = cfg.get('email_credentials', 'username')
export_data_request_url = cfg.get('other_settings', 'export_data_request_url') + ("&user_email=%s&user_name=%s" %(email_address, username))


# check if export request has been made already
date_today = datetime.now().strftime('%Y%m%d')
try:
  infile = open('qb_export_data_request_time', 'r')
  timestamp = infile.read()
  infile.close()
  if (search(date_today, timestamp)):
    print "Request has been made already. Please wait for the email to be delivered."
    exit(0)
except IOError:
  import traceback
  print traceback.format_exc()

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
driver.find_element_by_id('LoginButton').click()

driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])

# print "export_data_request_url: %s" %export_data_request_url
print "Requesting data..."
time.sleep(10)
driver.get(export_data_request_url)

time.sleep(60)
# write the timestamp for the request (to make sure that the request made for the day will not be forgotten)
outfile = open('qb_export_data_request_time', 'w')
outfile.write(date_today)
outfile.close()
print "Request for today has been recorded."

driver.get(url)
time.sleep(30)
driver.switch_to_default_content()
driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
time.sleep(2)
print "Signing out"
driver.find_element_by_link_text('Sign Out').click()
time.sleep(10)
driver.quit()
exit(0)
