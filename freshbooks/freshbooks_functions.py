import os
import ConfigParser
import time
import re
import logging
import pdb

cfg = ConfigParser.ConfigParser()
cfg.read('freshbooks-dump.cfg')


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
