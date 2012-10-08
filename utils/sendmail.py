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
    print c.read(cfg)
    print c.get('email', 'sender_uname')
  if message:
    print "message =", message

  # global cfg
  uname = c.get('email', 'sender_uname')
  pword = c.get('email', 'sender_pword')
  toaddr = c.get('email', 'toaddr')

  s = smtplib.SMTP(c.get('email', 'smtp_server'))

  # transform msg param to a MIMEText instance
  mimetext_msg = MIMEText(message)
  mimetext_msg['From'] = 'Cascadeo SPOF <' + uname + '>'
  mimetext_msg['To'] = toaddr
  mimetext_msg['Subject'] = 'FreshBooks dump finished.'

  print s.starttls()
  print s.login(uname, pword)
  print s.sendmail(uname, toaddr, mimetext_msg.as_string())
  print s.quit()
  exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cfg", help="Config file to use in sending email")
parser.add_argument("-m", "--message", help="Parameters to pass", type=str)


args = parser.parse_args()
print args
email(args.cfg, args.message)
# usage: email('Some message....', 'johndoe.foobar@example.com')
