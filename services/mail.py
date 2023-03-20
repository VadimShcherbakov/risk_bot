import os
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version


def mail( post_text: str) -> None:

    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login('pgva@bk.ru', 'C9BFX3ssXduN6W15kSmB')

    mail.list()
    print('Подключение к почте - успешно', mail.select("inbox"))
    server = 'smtp.mail.ru'
    user = 'pgva@bk.ru'
    password = 'C9BFX3ssXduN6W15kSmB'

    recipients = ['scherbakovvp@mosenergo.ru']
    sender = 'pgva@bk.ru'
    subject = 'Устранение рисков'
    text = f'Добрый день! У вас есть {post_text}. Таблица рисков  в приложении к письму:'
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    main_table = MIMEText('<h3>Таблица рисков</h3>', 'html')

    filepath = "таблица_рисков.xlsx"
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
    msg.attach(main_table)


    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    print('Письмо отправлено')



