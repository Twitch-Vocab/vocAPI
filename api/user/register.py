from utils.mid import *
from mdb import *
from typing import Dict

import time
import traceback
from email.utils import parseaddr

register_enabled = True
try:
    import passlib.hash
    from passlib import pwd
except (ModuleNotFoundError, ImportError):
    print("PASSLIB IMPORT FAILED")
    register_enabled = False

from db import user_ops
from db import config_ops
from db import session_mgr

from utils import check_type
from utils.graylog import LogWriter

from utils.reply import any_messages


def register(message: Dict[any, any]) -> Dict[any, any]:

    if not register_enabled:
        LogWriter.alert("register_used_but_disabled")
        return {any_messages.result: False,
                any_messages.reason: "server_function_disabled"}

    password = message.get("password", "")
    email = message.get("email", "")
    accept_tos = message.get("accept_tos", False)
    accept_data = message.get("accept_data", False)
    
    check_type.assert_str(password, "password")
    check_type.assert_str(email, "email")
    check_type.assert_bool(accept_tos, "accept_tos")
    check_type.assert_bool(accept_data, "accept_data")

    user_email = parseaddr(email)[1]
    organisation_id = "" 
    password_hash = passlib.hash.md5_crypt.hash(password)
    firstname = ""
    lastname = ""
    config_doc = {}

    #basic checks
    if not accept_tos:
        return {any_messages.result: False,
                any_messages.reason: "tos_not_accepted",
                any_messages.reason_nice: "Please accept the TOS."}

    if not accept_data:
        return {any_messages.result: False,
                    any_messages.reason: "data_not_accepted"}
    
    if not password:
        return {any_messages.result: False,
                any_messages.reason: "empty_password"}
    
    domain = user_email.split('@')[1]
    if not user_email or not domain:
        return {any_messages.result: False,
                any_messages.reason: "email_invalid"}
                    
    test_user_doc = user_ops.get_user_by_email(user_email)
    if test_user_doc:
        return {any_messages.result: False,
                any_messages.reason: "user_already_exists"}
    
    # if not invitation_doc: 
    print("user_email " + user_email)
    print("password_hash " + password_hash)

    config_doc = config_ops.get_default_config()
        
    #TODO: add user document
    user_id = MID.rand().str
    user_doc = {dbns.user.user_id: user_id,
                dbns.user.email: user_email,
                dbns.user.email_confirmed: False,
                dbns.user.password: password_hash,
                dbns.user.created: int(time.time()),
                dbns.user.modified: int(time.time()),
                #dbns.user.lastlogin: int(time.time()),
                dbns.user.lastname: "",
                dbns.user.firstname: ""}
    mdb.user().insert_one(user_doc)

    print("USER " + str(user_doc))

    session_id = session_mgr.session_create(user_id)
    return {any_messages.result: True,
            "session_id": session_id}


def send_password_mail(user_email: str, password: str):
    try:                                            
        message = {dbns.mail_templates.lang: "en",
                   dbns.mail_templates.mail_type: "registration_password",
                   "receivers": [user_email],
                   dbns.mail_templates.placeholders: {
                                            "user_name": username,
                                            "password": password}}        
        mail_result = mailHelper.mail(message, MID().rand().str)
    except:            
        traceback.print_exc()