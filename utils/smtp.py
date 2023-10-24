import smtplib

from data.config import *


def send_email(email, text):
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    server.login(SMTP_LOGIN, SMTP_PASSWORD)
    letter = templates['email_template'].format(from_mail=SMTP_EMAIL, to_mail=email, name=SMTP_NAME, data=text)
    letter = letter.encode("utf-8")
    server.sendmail(SMTP_EMAIL, email, letter)
    server.quit()