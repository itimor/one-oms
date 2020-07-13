# -*- coding: utf-8 -*-
# author: itimor

from celery import shared_task
from time import sleep


@shared_task
def add(x, y):
    sleep(30)
    return x + y


@shared_task
def send_mail(subject, mail_to, mail_host, mail_user, mail_password, content):
    import smtplib
    from email.mime.text import MIMEText
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = mail_user
    message['To'] = mail_to[0:]
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_password)
        smtpObj.sendmail(mail_user, mail_to, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)


@shared_task
def send_telegram(token, chat_id, content):
    import telegram
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=content)
