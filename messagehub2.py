from pymongo import MongoClient
from typing import Dict, Tuple, List

import sys
import traceback
import socket
import time
#import graphyte

from utils.mid import MID
from utils.graylog import LogWriter
from utils.config import Config
from utils import check_type
from utils.tictoc import TicToc
from utils.reply import any_messages

from db import session_mgr


from api.user import login
from api.user import register
from api.user import passwordforgotten

from api import userHandler 
from api import twitchexHandler

#SANIC
from sanic.response import StreamingHTTPResponse
from sanic.response import HTTPResponse
from sanic import response


async def handleMessage(message: dict, headers: dict, module:str, action: str, ip:str = ""):
    reply = {}
    status = 200
    timer = TicToc()
    url = ""

    if "/" in action:
        url_blocks = action.split("/")
        action = url_blocks.pop(0)
        url = "/".join(url_blocks )
        print("!!!!! " + url)

    try:        
        print("[HUB] module: " + module)
        print("[HUB] action: " + action)
        print("[HUB] headers: " + str(headers))
        print("MESSAGE" + str(message))
        is_known = False

        #AUTHENTICATE THE USER AND REPLY WITH FAILURE IF UNSUCCESSFULL
        user_doc = twitchexHandler.authenticate(message, headers)
        if not user_doc:
            reply = {any_messages.result: False,
                     any_messages.reason: "authentication_failed"}
            status = 401
        
        #NORMAL MODULES
        #MOD USER
        if user_doc and module == "twitchex":
            reply = twitchexHandler.handle(action, message, headers)
            is_known = True

        if not is_known and not reply: 
            reply = {any_messages.reason: "unkown_type",
                     any_messages.result: False}
        
    except check_type.BadTypeError:
        err_str = traceback.format_exc()
        LogWriter.alert("bad_types_error", {"exc": err_str})
        traceback.print_exc()

        status = 400
        return {any_messages.result: False,
                any_messages.reason: "bad_types_error"}, status

    except:        
        err_str = traceback.format_exc()
        print(err_str)
        LogWriter.alert("internal_server_error", {"exc": err_str, "mod":module, "act": action, "ip": ip})
        
        status = 500
        return {any_messages.result: False,
                any_messages.reason: "internal_server_error"}, status

    #print("logging: " + str(Config.log_requests))
    reply_str = str(reply)[:200]
    print("[HUB REPLY] " + reply_str)
    request_time_ms = timer.end()
    
    print("SENDING GRAYLOG #############################")
    LogWriter.info("/" + module + "/" + action + "/", {"mod":module, "act": action, "reply": reply_str, "headers": str(headers), "duration_ms": request_time_ms, "ip": ip})

        #try:
        #    graphyte.send("req." + module + "." + action + ".duration_ms", request_time_ms)
        #except:
        #    traceback.print_exc()

    return reply, status
