import os
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version
from config_data.config import *


#Модуль для отправки писем
def mail(post_text: str, filepath: str) -> None:
    config: Config = load_config()
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(config.mail_data.mail_user, config.mail_data.mail_password)

    mail.list()
    # print('Подключение к почте - успешно', mail.select("inbox"))
    server = 'smtp.mail.ru'
    user = config.mail_data.mail_user
    password = config.mail_data.mail_password

    recipients = [config.mail_data.mail_recipients]
    sender = config.mail_data.mail_user
    subject = post_text
    text = f'Добрый день! У вас есть {post_text}.'
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    basename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Vadim_Shcherbakov <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())


    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    part_file.set_payload(open(filepath, "rb").read())
    part_file.add_header('Content-Description', basename)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    encoders.encode_base64(part_file)

    msg.attach(part_text)
    msg.attach(part_html)
    msg.attach(part_file)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    # print('Письмо отправлено')



