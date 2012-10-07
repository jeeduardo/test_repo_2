import smtplib
import argparse
import ConfigParser
from email.mime.text import MIMEText


#cfg = ConfigParser.ConfigParser()
#
#cfg.read('lpdump.cfg')


# 'encrypted' SECRET + generated random key, not yet to be sent
# added enc_filename (for the subject)

def email(cfg, message):
  # for the meantime
  if cfg:
    print "cfg =", cfg
    c = ConfigParser.ConfigParser()
    c.read(cfg)
    print c.get('email', 'sender_uname')
  if message:
    print "message =", message

  return False
#  # global cfg
#  uname = cfg.get('email', 'sender_uname')
#  pword = cfg.get('email', 'sender_pword')
#
#  s = smtplib.SMTP(cfg.get('email', 'smtp_server'))
#
#  # transform msg param to a MIMEText instance
#  mimetext_msg = MIMEText(msg)
#  mimetext_msg['From'] = 'Cascadeo SPOF <' + uname + '>'
#  mimetext_msg['To'] = toaddr
#  mimetext_msg['Subject'] = 'FreshBooks dump finished.'
#
#  print s.starttls()
#  print s.login(uname, pword)
#  print s.sendmail(uname, toaddr, mimetext_msg.as_string())
#  print s.quit()
  exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cfg", help="Config file to use in sending email")
parser.add_argument("-m", "--mmessage", help="Parameters to pass", action='append', type=str)


args = parser.parse_args()
print args
email(args.cfg, args.message)
# usage: email('Some message....', 'johndoe.foobar@example.com')
