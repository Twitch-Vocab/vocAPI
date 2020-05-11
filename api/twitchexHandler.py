from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from utils.mid import MID

from db import session_mgr


from api.twitchex import hello

from utils.reply import any_messages

messagetypes = ['hello']

def handle(action: str, message: Dict[any, any]) -> Dict[any, any]:
       
    if not action in messagetypes:
        reply = {any_messages.reason: "unkown_type",
                 any_messages.result: False}
        return reply

    if action == "hello":
        return hello.hello(message)

    return {}