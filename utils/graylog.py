
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging

from utils.config import Config
from utils.mid import MID
from typing import Text 
from typing import List 
from typing import Dict 

import socket
import traceback

class LogWriter:
    logger = logging.Logger("GRAYLOG")


    @classmethod
    def setup(cls):
        if not Config.graylog_enable:
            print("GRAYLOG SETUP (DISABLED)")
            return

        print("LOG SETUP")
        logging.basicConfig(level=logging.FATAL)
        cls.handler = GelfUdpHandler(host=Config.graylog_addr, port=Config.graylog_port, include_extra_fields=True)
        cls.handler.domain = socket.gethostname()
        print("logging domain: " + cls.handler.domain)
        cls.logger.addHandler(cls.handler) 
        

    @classmethod
    def info(cls, message: str, tags: Dict[str, str] = {}):  
        if not Config.graylog_enable:
            print("GRAYLOG DISABLED " + message + " " + str(tags))
            return

        print("GRAYLOG >>> " + message + " " + str(tags))

        try:
            print(message)

            filtered_tags = {}
            if tags:
                for key, value in tags.items():
                    if isinstance(value, bool):
                        value = str(value)
                    filtered_tags.update({key: value})
                
            if filtered_tags:
                cls.logger.info(message, extra = filtered_tags)
            else:
                cls.logger.info(message)
                        
        except:
            traceback.print_exc()
            return


    @classmethod
    def alert(cls, message: str, tags: Dict[str, str] = {}):
        if not Config.graylog_enable:
            print("GRAYLOG DISABLED " + message + " " + str(tags))
            return

        tags.update({"full_message": message})
        tags.update({"alert": True})
        cls.info("ALERT", tags)