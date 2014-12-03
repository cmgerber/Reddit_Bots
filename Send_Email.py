#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Author: Colin Gerber

__version__ = 1.0

import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from calendar import monthrange
from email import Encoders
import time
import config


def send_mail(send_from, send_to, subject, text, smtp, files=[]):
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEApplication(open(f, 'rb').read())
        part.add_header(
            'Content-Disposition',
            'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    server = smtplib.SMTP(smtp)
    server.ehlo()
    server.starttls() #n
    server.login(config.email['username'], config.email['password']) #n
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()


def main(email_text, recipients):


    date = time.strftime("%m/%d/%Y")
    subject = 'Reddit Author bot Update %s' % (date)
    text = email_text

    send_from = 'colinRedditBot@gmail.com'
    send_to = recipients
    files = []
    smtp ='smtp.gmail.com:587'
    send_mail(send_from, send_to, subject, text, smtp, files)

    #print 'Email Sent'

if __name__ == "__main__":
    main()
