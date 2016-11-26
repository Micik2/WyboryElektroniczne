#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import smtplib

hash = random.getrandbits(128)
print "hash value: %032x" % hash
h = "%032x" % hash

link = "127.0.0.1:5000/signup/" + str(h)
  
wiadomosc = ["From: Wybory Elektroniczne", 
"To: /gmail/", 
"Subject: Rejestracja na Wyborcę",
"",
"Aby dokończyć rejestrację kliknij w link poniżej:",
link]

msg = "\r\n".join(wiadomosc)#[
  #"From: WyboryElektroniczne",
  #"To: /gmail/",
  #"Subject: Rejestracja na Wyborcę",
  #"",
  #"Why, oh why"
  #])

fromaddr = 
toaddrs  = 
#msg = 'Why,Oh why!'
username = 
password = 
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()