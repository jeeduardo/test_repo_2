import smtplib
import argparse
import ConfigParser
import enc_pwd
import os
import logging
from email.mime.text import MIMEText


# 'encrypted' SECRET + generated random key, not yet to be sent
# added enc_filename (for the subject)

# TO-DO: enable logging
def email(cfg, subject, message):
  exit_code = 0 #default
  if cfg:
    c = ConfigParser.ConfigParser()
    print cfg
    print c.read(cfg)
    c.get('email', 'sender_uname')
  else:
    print "Cannot find config file %s" %(cfg)

  # global cfg
  uname = c.get('email', 'sender_uname')
  pword = enc_pwd.decrypt_pword(c.get('email', 'sender_pword'), os.path.dirname(os.path.realpath(cfg))+os.sep)

  # pword = c.get('email', 'sender_pword')
  toaddr = c.get('email', 'toaddr')

  s = smtplib.SMTP(c.get('email', 'smtp_server'))

  # transform msg param to a MIMEText instance
  mimetext_msg = MIMEText(message)
  mimetext_msg['From'] = 'Cascadeo SPOF <' + uname + '>'
  mimetext_msg['To'] = toaddr
  # mimetext_msg['Subject'] = 'FreshBooks dump finished.'
  mimetext_msg['Subject'] = subject

  try:
    print "Preparing to send email to %s with subject \"%s\"" % (toaddr, subject)
    s.starttls()
    s.login(uname, pword)
    s.sendmail(uname, toaddr, mimetext_msg.as_string())
    s.quit()
  except:
    import traceback
    tb = traceback.format_exc()
    print "Something went wrong:"
    print tb
    exit_code = 1

  if (exit_code > 0):
    exit(exit_code)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--cfg", help="Config file to use in sending email")
  parser.add_argument("-s", "--subject", help="Subject of the email you will send.", type=str)
  parser.add_argument("-m", "--message", help="Message of the email you will send.", type=str)
  
  
  args = parser.parse_args()
  if args.cfg and args.subject and args.message:
    email(args.cfg, args.subject, args.message)
  else:
    print "Insufficient parameters."
    exit(1)
  # usage: email('Some message....', 'johndoe.foobar@example.com')
