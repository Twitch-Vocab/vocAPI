from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

try:
    import passlib.hash
    from passlib import pwd
except (ModuleNotFoundError, ImportError):
    print("PASSLIB IMPORT FAILED")
    register_enabled = False


from mdb import mdb
from mdb import dbns

from utils.mid import MID

from utils.graylog import LogWriter

from db import session_mgr
from db import user_ops

#email format checking
from email.utils import parseaddr

from utils.reply import any_messages

def login(message: Dict[any, any]):
    
    #get desired duration - default 10min
    session_duration = message.get("session_duration", 600)

    email_submitted = message.get("email", "")
    email_parsed = parseaddr(email_submitted)[1]
    user_pw = message.get("password", "")
    print("PARSED MAIL: " + email_parsed)
    if not email_parsed or not "@" in email_parsed:
        return {any_messages.result: False,
                any_messages.reason: "bad_email",
                any_messages.reason_nice: "Invalid Email."}
    
    user = user_ops.get_user_by_email(email_submitted)
    
    if not user:
        return {any_messages.result: False,
                any_messages.reason: "user_not_found"}

    if not email_submitted.lower() == user.get(dbns.user.email,"").lower():
        return {any_messages.result: False,
                any_messages.reason: "login_failed"}
        
    user_id = MID(user[dbns.user.user_id])
    if not user_id.valid:
        return {any_messages.result: False,
                any_messages.reason: "login_failed"}
    
    login_success = False
    
    salt = user.get(dbns.user.password,"")[3:11]
    user_pw_hash = passlib.hash.md5_crypt.hash(user_pw, salt=salt)
    login_success = user[dbns.user.password] == user_pw_hash
        
    if not login_success:
        return {any_messages.result: False,
                any_messages.reason: "login_failed"}
        
    session_id = session_mgr.session_create(user_id.str, session_duration)
    
    reply = {any_messages.result: login_success,
             "session_id": session_id}

    return reply


