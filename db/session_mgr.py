from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from utils.mid import MID

from mdb import *
from db import user_ops



def get_session_id(session_doc: Dict[any, any]):
    return session_doc.get(dbns.user_sessions.session_id, "")


def get_user_id(session_doc: Dict[any, any]):
    return session_doc.get(dbns.user_sessions.user_id, "")


def get_user_doc(session_doc: Dict[any, any]):
    return session_doc.get("user_doc", {})


def session_check(session_id: str) -> str:
    #get nodes of this user
    session_filter = {dbns.user_sessions.session_id: session_id}
    
    session_doc = mdb.user_sessions().find_one(session_filter)

    if not session_doc:
        return {}

    valid_until = session_doc.get(dbns.user_sessions.valid_until, 0)

    if int(time.time()) > valid_until:
        return {}
        
    #add user doc for normal sessions
    user_id = get_user_id(session_doc)    
    user_doc = user_ops.get_user_by_id(user_id)
    session_doc.update({"user_doc": user_doc})

    return session_doc


def session_create(user_id: str, duration: int = 3600) -> str:
    if not user_id:
        return ""
    
    session_id = MID.rand().str

    #max 24h
    if(duration > 86400):
        duration = 86400

    # create session id, write it to database
    one_session = {}

    one_session = {dbns.user_sessions.user_id: user_id,
                    dbns.user_sessions.session_id: session_id,
                    dbns.user_sessions.valid_until: int(time.time()) + duration}
                
    mdb.user_sessions().insert_one(one_session)
        
    #clean up old user sessions
    user_sessions_filter = {dbns.user_sessions.valid_until: {"$lt": int(time.time())}}
    mdb.user_sessions().delete_many(user_sessions_filter)

    return session_id


def session_renew(session_id: str, duration: int = 3600) -> str:
    session_doc = session_check(session_id)

    user_id = get_user_id(session_doc)
    if session_doc:
        return session_create(user_id, duration)

    return ""


def session_delete(session_id: str) -> str:        
    mdb.user_sessions().delete_one({dbns.user_sessions.session_id: session_id})        
    return True        
