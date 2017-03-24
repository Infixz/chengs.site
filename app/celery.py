# coding: utf-8

from __future__ import absolute_import
from celery import Celery
from .local_settings import current_env as env


##
# celery app
##
app = Celery('chengs.site')
app.config_from_object(env)


##
# celery tasks
##

import smtplib
from email.mime.text import MIMEText
from email.Header import Header


@app.task
def send_email(receivers, subject, content, sender='admin@chengs.site'):
    """
    receivers can be str or list of str
    """
    # build msg
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = Header(subject, charset='UTF-8')
    # smtp part
    smtp_server = smtplib.SMTP_SSL(env.MAIL_SERVER, env.MAIL_PORT)
    smtp_server.login(env.MAIL_USERNAME, env.MAIL_PASSWORD)
    smtp_server.sendmail(env.MAIL_USERNAME, receivers, msg.as_string())
    smtp_server.quit()
