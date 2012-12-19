#!/usr/bin/python
import os
import rsa
import base64
import argparse
import re
import time
from datetime import datetime

# key_dir - directory where the private key will be stored
# defaults to current path if not supplied
def encrypt_pword(pword, key_dir=None):

  # set to current path if dir wasn't supplied
  if (key_dir == None):
    key_dir = os.getcwd() + os.sep

  privkey_filename = "%s/privkey.pem" %(key_dir)
  pubkey_filename = "%s/pubkey.pem" %(key_dir)

  # generate private pubkey key pair
  if (os.path.exists(privkey_filename) and time.strftime('%m%d%Y', time.localtime()) == time.strftime('%m%d%Y', time.localtime(os.path.getctime(privkey_filename)))):
    print "Key/s exist for the day. I'm not creating one."
  else:
    # use os.path.dirname(os.path.realpath(incomplete_path_to_file))
    os.system("openssl genrsa -out %s 512" %(privkey_filename))


  os.system("pyrsa-priv2pub -i %s -o %s" %(privkey_filename, pubkey_filename))
  
  with open(pubkey_filename, 'r') as pubkey_file:
    pubkey_data = pubkey_file.read()
  pubkey_file.close()

  pub = rsa.PublicKey.load_pkcs1(pubkey_data)
  enc_pword = rsa.encrypt(pword, pub)
  b64_enc_pword = base64.b64encode(enc_pword)
  os.system("rm -f %s" %(pubkey_filename))
  p = os.popen("echo $(cut -c1 < %s) | sed 's/[\ |-]//g'" %(privkey_filename))
  pphrase = p.read().strip()
  enc_p = os.popen("echo '%s' | openssl enc -aes-256-cbc -a -salt -pass pass:%s" %(b64_enc_pword, pphrase))
  aes_enc_pword = enc_p.read().strip()

  # chmod private key file
  import stat
  os.chmod(privkey_filename, stat.S_IREAD + stat.S_IWRITE)
  return aes_enc_pword.replace('\n', '')


def decrypt_pword(p_pword, key_dir=None):

  if (key_dir == None):
    key_dir = os.getcwd() + os.sep

  privkey_filename = "%sprivkey.pem" %(key_dir)
  pword = ''
  p = os.popen("echo $(cut -c1 < %s) | sed 's/[\ |-]//g'" %privkey_filename)
  pphrase = p.read().strip()
  p.close()
  fp_pword = re.sub("(.{64})", "\\1\n", p_pword, re.DOTALL)

  tmp_file = "%senc_pword.temp.txt" %(key_dir)
  fp_pword_file = open(tmp_file, 'w')
  fp_pword_file.write(fp_pword)
  fp_pword_file.close()

  p = os.popen("openssl aes-256-cbc -in %s -d -a -pass pass:%s" %(tmp_file, pphrase))
  b64_enc_pword = p.read().strip()
  enc_pword = base64.b64decode(b64_enc_pword)
  with open(privkey_filename, 'r') as privkey_file:
    privkey_data = privkey_file.read()
  privkey_file.close()

  priv = rsa.PrivateKey.load_pkcs1(privkey_data)
  pword = rsa.decrypt(enc_pword, priv)

  os.system("rm -f %s" %(tmp_file))
  return pword

