from pymongo import MongoClient
from typing import Dict, Tuple, List
import time

from mdb import mdb
from mdb import dbns

from utils.graylog import LogWriter

from utils.reply import any_messages

def hello(message: Dict[any, any]):
    

    return {any_messages.result: True,
            "hello": "hello"}


