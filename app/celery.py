# coding: utf-8

from __future__ import absolute_import
import smtplib
import email.MIMEBase
from email.Header import Header
from celery import Celery
from .local_settings import current_env as env


app = Celery('chengs.site')
app.config_from_object(env)


def _send_mail(receivers, html_content):
    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()
    # msg = MIMEMultipart()
    main_msg['From'] = 'infixz@foxmail.com'
    main_msg['To'] = ",".join(receivers)
    main_msg['Subject'] = Header('New user registed', charset='UTF-8')

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    html_msg = email.MIMEText.MIMEText(html_content, 'html')
    main_msg.attach(html_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    # contype, encoding = mimetypes.guess_type(file_name)
    # maintype, subtype = contype.split('/', 1)

    smtp = smtplib.SMTP_SSL()
    smtp.connect(env.MAIL_SERVER+':'+str(env.MAIL_PORT))
    smtp.login(env.MAIL_USERNAME, env.MAIL_PASSWORD)
    smtp.sendmail(env.MAIL_USERNAME, receivers, main_msg.as_string())
    smtp.quit()


##
# celery tasks
##


@app.task
def send_mail():
    pass


@app.task
def reg_notice_admin(html_content):
    recipients = [env.ADMIN_EMAIL]
    _send_mail(recipients, html_content)
