import os
import sys
from smtplib import SMTPException
from datetime import datetime
from flask_mail import Message

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
from app.main import mail, app
from app.libs.email_templates import reset_password_template


# def send_invite_user_mail(email="none", first_name="", password="",username=""):
#     try:
#         msg = Message(subject=f'Welcome to Sibyl',
#                       sender=MAIL_USERNAME, recipients=[email])
#         msg.html = invite_user_template(first_name, username, password)
#         mail.send(msg)
#         return 0
#     except SMTPException as smtpex:
#         print("************************************** Exception is :{}".format(smtpex))
#         return 1
    
    
def send_reset_password_email(email="none", first_name="", temp_password=""):
    try:
        msg = Message(subject=f'Password Reset Request',
                      sender=MAIL_USERNAME, recipients=[email])
        msg.html = reset_password_template(first_name, temp_password)
        mail.send(msg)
        return 0
    except SMTPException as smtpex:
        print("************************************** Exception is :{}".format(smtpex))
        return 1
