
import re
import copy
from pymongo import MongoClient
from typing import Dict, Tuple, List

from utils.mid import MID

from mdb import mdb
from mdb import dbns


def get_users_by_ids(user_ids: List[str], projection: Dict[any, any] = {}) -> Dict[any, any]:
    filter = {dbns.user.user_id: {"$in": user_ids}}
    projection.update({'_id':False})
    docs = mdb.user().find(filter, projection)

    doc_list = []
    for one_doc in docs:
        doc_list.append(one_doc)

    return doc_list


def get_user_by_id(user_id: str) -> Dict[any, any]:
    user_filter = {dbns.user.user_id: user_id}
    user = mdb.user().find_one(user_filter)
    if not user:
        return {}
    return user


def get_user_by_email(mail: str) -> Dict[any, any]:
    email_regx = re.compile(mail.lower(), re.IGNORECASE)
    user_filter = {dbns.user.email: email_regx}
    user_result = mdb.user().find(user_filter)
    user = {}
    for one_user in user_result:
        if one_user.get(dbns.user.email, "").lower() == mail.lower():
            user = copy.deepcopy(one_user)
    if not user:
        return {}
    return user
