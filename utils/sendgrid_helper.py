import traceback
import smtplib
import os
from email.message import EmailMessage

#sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utils.graylog import LogWriter

from mdb import *


def get_api_key():
    
    config_doc = mdb.config().find_one()
    api_key = config_doc.get(dbns.config.sendgrid_api_key, "")

    if not api_key:
        LogWriter.alert("NO_MAIL_API_KEY")

    return api_key


def send_mail(subject: str, content: str, content_html: str, toAddr: str):

    api_key = get_api_key()
    mail_from_addr = "info@rimworld.me"

    print("MAIL KEY " + api_key)

    message = Mail(
    from_email=mail_from_addr,
    to_emails=toAddr,
    subject=subject,
    html_content=content_html)
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except:
        traceback.print_exc()

