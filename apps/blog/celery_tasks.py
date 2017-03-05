# coding: utf-8

from celery_main import app
from local_settings import MAIL_SERVER, MAIL_PORT,\
        MAIL_USERNAME, MAIL_PASSWORD
import smtplib
import email.MIMEBase
from email.Header import Header


def send_mail(receivers, html_content):
    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()
    # msg = MIMEMultipart()
    main_msg['From'] = 'infixz@foxmail.com'
    main_msg['To'] = ",".join(receivers)
    main_msg['Subject'] = Header('New user', charset='UTF-8')

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    html_msg = email.MIMEText.MIMEText(html_content, 'html')
    main_msg.attach(html_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    # contype, encoding = mimetypes.guess_type(file_name)
    # maintype, subtype = contype.split('/', 1)

    smtp = smtplib.SMTP_SSL()
    smtp.connect(MAIL_SERVER+':'+str(MAIL_PORT))
    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
    smtp.sendmail(MAIL_USERNAME, receivers, main_msg.as_string())
    smtp.quit()


@app.task
def reg_notice(html_content):
    recipients = ['sorrible@126.com']
    send_mail(recipients, html_content)
