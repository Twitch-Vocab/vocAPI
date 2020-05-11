from utils.mid import *
from mdb import *
from typing import Dict

from db import user_ops
from utils import check_type
from utils.reply import any_messages
from utils.graylog import LogWriter
import traceback

reset_enabled = True
try:
    import passlib.hash
    from passlib import pwd
except (ModuleNotFoundError, ImportError):
    print("PASSLIB IMPORT FAILED")
    reset_enabled = False


def passwordforgotten(message: Dict[any, any]) -> Dict[any, any]:
    if not reset_enabled:
        LogWriter.alert({"full_message":"register_used_but_disabled"})
        return {any_messages.result: False,
                any_messages.reason: "server_function_disabled"}

    email = message.get("email", "")
    check_type.assert_str(email, "email")

    if not email:
        return {any_messages.result: False,
                any_messages.reason: "user_email_empty"}

    user_doc = user_ops.get_user_by_email(email)
    
    if not user_doc:
        return {any_messages.result: False,
                any_messages.reason: "user_not_exists"}
    
    password = pwd.genword()    
    password_hash = passlib.hash.md5_crypt.hash(password)
    
    email = user_doc.get(dbns.user.email, "")
    username = user_doc.get(dbns.user.username, "")

    send_password_mail(email, username, password)

    if result:
        return {any_messages.result: True}


def send_password_mail(user_email: str, username: str, password: str):
    try:                                            
        message = {dbns.mail_templates.lang: "en",
                dbns.mail_templates.mail_type: "forgotten_password",
                "receivers": [user_email],
                dbns.mail_templates.placeholders: {
                                            "user_name": username,
                                            "password": password}}        
        #mail_result = mailHelper.mail(message, MID().rand().str)
    except:            
        traceback.print_exc()