import smtplib
import argparse
import ConfigParser
from email.mime.text import MIMEText


#cfg = ConfigParser.ConfigParser()
#
#cfg.read('lpdump.cfg')


# 'encrypted' SECRET + generated random key, not yet to be sent
# added enc_filename (for the subject)

def email(cfg, subject, message):
  # for the meantime
  if cfg:
    c = ConfigParser.ConfigParser()
    print cfg
    print c.read(cfg)
    c.get('email', 'sender_uname')

  # global cfg
  uname = c.get('email', 'sender_uname')
  pword = c.get('email', 'sender_pword')
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
    exit(1)
  exit(0)

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
