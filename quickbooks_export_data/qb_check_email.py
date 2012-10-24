#!/usr/bin/python
from datetime import datetime, timedelta
import time
import imaplib
import email
import re
from ConfigParser import ConfigParser
import logging
import os


def get_body(payload):
  if isinstance(payload, str):
    return payload
  else:
    return '\n'.join([get_body(part.get_payload()) for part in payload])
  return payload

# get config
cfg = ConfigParser()
cfg.read('qb_export_data.cfg')

# set up logging
logging.basicConfig(filename=os.getcwd() + os.sep + cfg.get('other_settings', 'log_file'), level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')

# set up login
username = cfg.get('email_credentials', 'username')
pword = cfg.get('email_credentials', 'pword')
search_term = cfg.get('email_credentials', 'search_term')


mail = imaplib.IMAP4_SSL(cfg.get('email_credentials', 'imap_host'))
logging.info("Logging in as %s" %(username))
mail.login(username, pword)
mail.select("inbox")
# to do : search emails according to search_term
#result, data = mail.search(None, "ALL")
# result, data = mail.search(None, "UNSEEN")
result, msgdata = mail.uid('search', None, '(HEADER Subject "%s")' %(search_term))
try:
  ids = msgdata[0]
  id_list = ids.split()
  latest_id = id_list[-1]
  result2, msgdata = mail.fetch(latest_id, '(RFC822)')
  for response_part in msgdata:
    try:
      msg = email.message_from_string(response_part[1])
      subject = msg['subject']
      payload = msg.get_payload()
      body = get_body(payload)
  
      # if (re.search(search_term, subject)):
      #logging.info("Found email with subject \"%s\"" %(subject))
      mail_timestamp = msg['date'][5:25]
      # check if this was sent within the day
      mail_datetime = datetime.strptime(mail_timestamp, '%d %b %Y %H:%M:%S')
      # TO-DO: use something like datetime.now() - timedelta(hours=8?) since gmail account is on PDT!
      pdt_curr_datetime = datetime.now() - timedelta(hours=7)
      # print mail_datetime, "AND", pdt_curr_datetime
      if (mail_datetime.day == pdt_curr_datetime.day):
        print "FOUND"
        logging.info("Got the email today from QuickBooks.")
        logging.info("Will fetch the exported data.")
      else:
        print "NOT FOUND"
        logging.info("Found email with subject \"%s\" but this is NOT the email today." %(subject))
        logging.info("Calling script to initiate export of data.")
        # 2 - No email for today. Issue request to export data."
    except:
      import traceback
      logging.error(traceback.format_exc())
      pass
except:
  import traceback
  logging.error(traceback.format_exc())
  exit(1)
finally:
  mail.close()
  logging.info('Signing out...')
  logging.info(mail.logout())

  exit

