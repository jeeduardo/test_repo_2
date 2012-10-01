import os
import ConfigParser
import time
import re
import logging
import pdb
from selenium import webdriver
from datetime import datetime

cfg = ConfigParser.ConfigParser()
cfg.read('freshbooks-dump.cfg')
url = cfg.get('credentials', 'main_url')
username = cfg.get('credentials', 'username')
pw = cfg.get('credentials', 'pword')
base_backup_dirname = cfg.get('settings', 'backup_dir_name')
# 01Oct2012 - eliminate spaces in filename
#backup_dirname = base_backup_dirname + datetime.now().strftime('_%Y-%m-%d')
backup_dirname = base_backup_dirname.replace(' ', '') + datetime.now().strftime('_%Y-%m-%d')

# function to get CSV file
# don't wanna keep repeating myself
# @params p_disp_msg - message to display while downloading the file (i.e. 'downloading Tax Summary CSV (billed)...')
# @params p_driver - instance of the Firefox driver used to get the file
# @params p_pattern - pattern to use in displaying the name of the file downloaded and to be renamed
# @params p_url - url of file to download
# @params p_params - parameters to pass to the url used in downloading the file

def get_file(p_disp_msg, p_driver, p_pattern, p_url, p_params=''):
  global logging
  logging.info(p_disp_msg)
  p_driver.get(p_url + p_params)
  logging.info('File saved as %s' % get_csv_filename(p_pattern))
  return 0

def rename_file(pattern, filename, replace_with=''):
  global backup_dirname
  patternToCheck = pattern 
  # 01Oct2012 - eliminate spaces in filename
  mvCmd = "mv " + filename + " " + backup_dirname + "/" + base_backup_dirname.replace(' ', '') + pattern.replace(' ', '') + replace_with + "_" + datetime.now().strftime('%m-%d-%Y_%H%M%S') + ".csv"
  logging.info('executing "' + mvCmd + '"')
  res = os.system(mvCmd)
  return res

# use -lrt preferably or -rt
# if pattern left blank, it will get the name of latest csv file
def get_csv_filename(pattern=''):
  p = os.popen("ls -t " + base_backup_dirname + pattern + "*.csv | head -1")
  filename = p.readline().strip()
  p.close()
  return re.escape(filename)

def get_and_rename_file(pattern, replace_with=''):
  filename = get_csv_filename(pattern)
  if (rename_file(pattern, filename, replace_with) == 0):
    logging.info('File %s was successfully renamed' % filename)
  else:
    logging.error('Something went wrong with the moving of file. Please check %s', filename)


# get url branch under the 'export_urls' section
# @param subsection - subsection under export_urls (i.e. 'client_csv_url')
def get_csv_url(subsection):
  global cfg, url
  try:
    return url + cfg.get('export_urls', subsection)
  except ConfigParser.NoOptionError:
    print "NO SUCH SUBSECTION. RETURNING blank!"
    return ''

# firefox profile to use
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")


print "backup_dirname w/o spaces = %s" %(backup_dirname.replace(' ', ''))
