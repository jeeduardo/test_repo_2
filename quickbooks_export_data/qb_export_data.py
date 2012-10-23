#!/usr/bin/python
from selenium import webdriver
import os
import time
from datetime import datetime
import logging
import ConfigParser

# set up logging and parse the config
cfg = ConfigParser.ConfigParser()
cfg.read('qb_export_data.cfg')
logging.basicConfig(filename=os.getcwd() + os.sep + cfg.get('other_settings', 'log_file'), level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')
logging.info("Getting configurations...")

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
pword = cfg.get('credentials', 'pword')

base_export_url = "https://qbo.intuit.com/qbo36-pprdqboas30m/export/download?file=true&timestamp="


try:
  driver = webdriver.Firefox()
  driver.get(url)
  time.sleep(10)
  
  login = driver.find_element_by_name('login')
  login.click()
  login.clear()
  login.send_keys(username)
  ppword = driver.find_element_by_name('password')
  ppword.click()
  ppword.clear()
  ppword.send_keys(pword)
  driver.find_element_by_id('LoginButton').click()
  logging.info("Logging in as %s" %(username))
  time.sleep(30)
  logging.info("Extracting data...")
  
  # get time in milliseconds
  # this is for the GET parameter sent when getting the data
  
  curr_time = datetime.now()
  first_time = datetime(1970, 1, 1, 0, 0, 1, 0)
  
  diff = curr_time - first_time
  
  ms = int((diff.days * 24 * 60 * 60 + diff.seconds) * 1000 + diff.microseconds / 1000.0)
  
  print "Milliseconds =", ms
  
  driver.get(base_export_url + str(ms))
  time.sleep(30)
  
  xml_dump = driver.page_source
  outfile_filename = "export_company_" + datetime.now().strftime('%Y%m%d_%H%M') + ".qbxml"
  outfile = open(outfile_filename, 'w')
  logging.info("Writing data to %s" %(outfile_filename))
  outfile.write(xml_dump)
  outfile.close()
  
  logging.info("Dump written to %s" %(outfile_filename))
  
  time.sleep(5)
  driver.get(url)
  time.sleep(30)
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  time.sleep(2)
  print "Signing out..."
  logging.info("Signing out...")
  driver.find_element_by_link_text('Sign Out').click()
  driver.quit()
  exit(0)
except:
  import traceback
  logging.error(traceback.format_exc())
  exit(1)
finally:
  logging.info("Exporting finished successfully.")
  exit(0)
