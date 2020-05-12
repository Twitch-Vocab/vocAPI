from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from mdb import mdb
from mdb import dbns

from utils.graylog import LogWriter

from utils.reply import any_messages

def hello(message: Dict[any, any], headers: Dict[any, any]):
    
    return {any_messages.result: True,
            "x-extension-jwt" : headers.get("x-extension-jwt", ""),
            "hello": "hello"}


