from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from utils.mid import MID

from db import session_mgr


from api.user import session_renew
from api.user import logout

from utils.reply import any_messages

messagetypes = ['session_renew',
                'logout']

def handle(message: Dict[any, any], action: str, session_doc: Dict[any, any], user_id: str) -> Dict[any, any]:
       
    session_id = session_mgr.get_session_id(session_doc)

    if not action in messagetypes:
        reply = {any_messages.reason: "unkown_type",
                 any_messages.result: False}
        return reply

    if action == "session_renew":
        return session_renew.session_renew(message, session_id)

    if action == "logout":
        return logout.logout(message, session_doc)

    return {}