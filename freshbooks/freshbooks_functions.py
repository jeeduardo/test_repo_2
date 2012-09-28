import os
import ConfigParser
import time
import re
import logging
import pdb
from selenium import webdriver

cfg = ConfigParser.ConfigParser()
cfg.read('freshbooks-dump.cfg')
url = cfg.get('credentials', 'main_url')
username = cfg.get('credentials', 'username')
pw = cfg.get('credentials', 'pword')


# use -lrt preferably or -rt
# if pattern left blank, it will get the name of latest csv file
def FF_get_csv_filename(pattern=''):
  # file is non-existent
  #p = os.popen("ls -t wackstest-cascadeo" + pattern + "*.csv | head -1")
  # the pattern below (i.e. "Trial Josephson (Cascadeo)")should be stored in the .cfg file
  # p = os.popen("ls -t Trial\ Josephson\ \(Cascadeo\)" + pattern + "*.csv | head -1")
  p = os.popen("ls -t Staging\ Backup\ Cascadeo" + pattern + "*.csv | head -1")
  filename = p.readline().strip()
  p.close()
  return re.escape(filename)

def FF_get_and_rename_file(pattern, replace_with=''):
  filename = get_csv_filename(pattern)
  # print 'latest csv file: %s' % filename
  if (rename_file(pattern, filename, replace_with) == 0):
    # print 'File %s was successfully renamed' % filename
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

