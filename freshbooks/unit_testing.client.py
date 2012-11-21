#!/usr/bin/python

import gdata.spreadsheet.service
import gdata.spreadsheet.text_db
from selenium import webdriver
from datetime import datetime
import time
import os
import re
from freshbooks_functions import fp, url, username, pw
import logging

# logging config
logging.basicConfig(filename=os.getcwd() + '/freshbooks.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

email = 'trial.freshbooks@gmail.com'
pword = 'M8q^*uf8$Y'
spreadsheet_key = '0ArlMFq1pwupIdEVQWHpNOXlwNk9zWG9VUTBxYUh2TUE'
# worksheet_id = 'od6'
worksheet_id = 'od7'
create_client_url = 'https://trialcascfb.freshbooks.com/menu.php?CB431CBcm91dGU9Y3JlYXRlVXNlckZCNTE3NDk='
create_timesheet_url = 'https://trialcascfb.freshbooks.com/menu.php?CB431CBcm91dGU9dGltZXNoZWV0RkI0OTQyNA=='

# open firefox
logging.info("opening firefox...")

try:
  driver = webdriver.Firefox(firefox_profile=fp)
  driver.get(url)

  driver.find_element_by_id('username').click()
  driver.find_element_by_id('username').send_keys(username)
  driver.find_element_by_id('password').click()
  driver.find_element_by_id('password').send_keys(pw)
  driver.find_elements_by_name('Submit')[2].click()
  time.sleep(5)

  spr_client = gdata.spreadsheet.service.SpreadsheetsService()
  spr_client.email = email
  spr_client.password = pword
  spr_client.ProgrammaticLogin()
except:
  import traceback
  tb = traceback.format_exc()
  print "ERROR! \n%s" %(tb)
  logging.error(tb)
  exit(1)

# functions
def find_click(element_id, value=None):
  global driver
  driver.find_element_by_id(element_id).click()
  if (isinstance(value, str)):
    driver.find_element_by_id(element_id).send_keys(value)
    time.sleep(3)

q = gdata.spreadsheet.service.ListQuery()

feed = spr_client.GetListFeed(spreadsheet_key, worksheet_id, query=q)

# add data
for row_entry in feed.entry:
  driver.get(create_client_url)
  time.sleep(5)
  row = gdata.spreadsheet.text_db.Record(row_entry=row_entry)
  print row.content


find_click('nav-log-out')
time.sleep(5)
del spr_client

