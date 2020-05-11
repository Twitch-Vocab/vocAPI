from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from db import session_mgr


from utils.reply import any_messages

#def session_renew(json: Dict[any, any], user_id: str) -> Dict[any, any]:
def session_renew(message: Dict[any, any], session_id: str) -> Dict[any, any]:
    
    keep_id = message.get("keep_id", False)
    #TODO
        
    session_duration = message.get("session_duration", 3600)
    session_id_new = session_mgr.session_renew(session_id, session_duration)
    
    if not session_id_new:
        return {any_messages.result: False,
                any_messages.reason: "session_renew_failed"}

    return {any_messages.result: True,
            "session_id": session_id_new}
