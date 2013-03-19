#!/usr/bin/python
from selenium import webdriver
import os
import time
from datetime import datetime, timedelta
import logging
import ConfigParser
import sys
sys.path.append(os.getcwd() + '/../utils')
import enc_pwd
import sendmail

# set up logging and parse the config
cfg = ConfigParser.ConfigParser()
cfg.read('qb_export_data.cfg')
logging.basicConfig(filename=os.getcwd() + os.sep + cfg.get('other_settings', 'log_file'), level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')
logging.info("Getting configurations...")

url = cfg.get('credentials', 'url')
username = cfg.get('credentials', 'username')
# 16Jan2013
# pword = enc_pwd.decrypt_pword(cfg.get('credentials', 'pword'), os.getcwd()+os.sep)
cmd_str = "./../utils/encpwd/read_cfg_pwd.sh ../../quickbooks_export_data/qb_export_data.cfg credentials pword"
pword = os.popen(cmd_str).readline().strip()

# base_export_url = "https://qbo.intuit.com/qbo36-pprdqboas30m/export/download?file=true&timestamp="
### RIGHT_base_export_url = "https://qbo.intuit.com/qbo28-pprdqboas30p/export/download?file=true&timestamp="

def get_export_results(export_url, ms):
  global driver
  export_url = export_url + str(ms)
  driver.get(export_url)
  logging.info("trying %s" %(export_url))
  time.sleep(5)
  
  xml_dump = driver.page_source
  import re
  xml_dump_list = xml_dump.split('\n')
  outfile_filename = "export_company_" + (datetime.now()-timedelta(hours=7)).strftime('%Y%m%d_%H%M') + ".qbxml"
  outfile = open(outfile_filename, 'w')
  outfile.write(xml_dump)
  outfile.close()
  time.sleep(5)

  if (re.search('404: File Not Found', xml_dump)):
    return (False, "NONE")
  if (len(xml_dump_list) > 2):
    logging.info("Dump written to %s" %(outfile_filename))
    return (True, outfile_filename)

  return (False, "NONE")

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
  
  # 03/15/2013 - loop to get to the RIGHT base_export_url starts here
  qb_version = cfg.get('other_settings', 'qb_version')
  is_correct = False
  first_time = datetime(1970, 1, 1, 0, 0, 1, 0)
  for nch in range(48, 58):
    base_export_url = "https://qbo.intuit.com/qbo%s-pprdqboas30%s/export/download?file=true&timestamp=" %(qb_version, chr(nch))
    # get time in milliseconds
    # this is for the GET parameter sent when getting the data
    
    curr_time = datetime.now()
    
    diff = curr_time - first_time
    
    ms = int((diff.days * 24 * 60 * 60 + diff.seconds) * 1000 + diff.microseconds / 1000.0)
    
    # 03/15/2013 - working on the changing url link
    ### print "THE URL: %s" %(base_export_url+str(ms))
    # get qb version
  
    ###     for nch in range(97, 122):
  
    ### print 10/0
    #  driver.get(base_export_url + str(ms))
    # 03/15/2013 - flag for checking correct download link
    is_correct, outfile_filename = get_export_results(base_export_url, ms)
    if is_correct:
      break

  if not is_correct:
    for nch in range(97, 122):
      curr_time = datetime.now()
      
      diff = curr_time - first_time
      
      ms = int((diff.days * 24 * 60 * 60 + diff.seconds) * 1000 + diff.microseconds / 1000.0)

      base_export_url = "https://qbo.intuit.com/qbo%s-pprdqboas30%s/export/download?file=true&timestamp=" %(qb_version, chr(nch))
      is_correct, outfile_filename = get_export_results(base_export_url, ms)
      if is_correct:
        break
    # 03/15/2013 work
  
  time.sleep(5)
  driver.get(url)
  time.sleep(30)
  driver.switch_to_default_content()
  driver.switch_to_frame(driver.find_elements_by_tag_name('iframe')[0])
  time.sleep(2)
  subject = "QuickBooks Data Dump has been extracted."
  msg = "Please check file %s for its contents." %(outfile_filename)
  sendmail.email(os.getcwd()+os.sep+'qb_export_data.cfg', subject, msg)
  ## logging.info("running this command - python %s/../utils/sendmail.py --cfg %s --subject \"QuickBooks Data Dump has been extracted.\" --message \"Please check file %s for its contents.\"" %(os.getcwd(), os.getcwd()+os.sep+'qb_export_data.cfg', outfile_filename))
  print "Signing out..."
  logging.info("Signing out...")

  driver.find_element_by_link_text('Sign Out').click()
  # time.sleep(5)
  # send email

  driver.quit()
### finally:
  print "Exporting finished successfully."
  logging.info("Exporting finished successfully.")
  # 03/19/2013 - delete "empty" dump files
  os.system(os.getcwd()+os.sep+'/delete_empty_qbxml.sh')
  logging.info("Exiting...")
  # TO-DO: inform people that QuickBooks dump has finished
  exit(0)
except:
  import traceback
  tb = traceback.format_exc()
  logging.error(tb)
  subject = "ERROR in QuickBooks Data Dump Script"
  msg = "An ERROR has been encountered with the script. Please see below traceback:\n%s" %(tb)
  sendmail.email(os.getcwd()+os.sep+'qb_export_data.cfg', subject, msg)
  exit(1)
