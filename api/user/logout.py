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

def logout(message: Dict[any, any], session_doc: Dict[any, any]):
    
    session_id = session_mgr.get_session_id(session_doc)

    session_mgr.session_delete(session_id)

    reply = {any_messages.result: True}

    return reply


