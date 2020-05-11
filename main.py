import os
import asyncio
import graphyte
import socket
import threading
import uvloop
import traceback
import sys
from sanic import Sanic
from sanic import response
from sanic.response import json as sanicJSON

#from utils import loops
#from utils.tictoc import TicToc

import mdb
import messagehub

from utils.config import Config
from utils.graylog import LogWriter

from jobs.jobs_mgr import *
from jobs import example_job

from local_cache import file_storage


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = Sanic()


#API - NORMAL ACCESS
@app.route('/<module>/<action:path>', methods=['POST','GET'])
async def handle_request(request, module, action):

    #get ip from nginx header or fallback to direct caller ip
    requester_ip = request.headers.get("x-real-ip", request.ip)

    reply_doc, status = await messagehub.handleMessage(request.json, request.headers, module, action, requester_ip)
    
    #return response.json({"session":session, "route":route, "one": one})
    reply = sanicJSON(reply_doc)
    reply.headers.update({"Access-Control-Allow-Origin": "*"})
    reply.status = status
    return reply


#API - NORMAL ACCESS - CORS
@app.route('/<module>/<action:path>', methods=['OPTIONS'])
async def handle_request(request, module, action):

    print("request:"+str(request.headers))
    origin = request.headers.get("origin","*")

    response = sanicJSON({})
    response.headers.update({"Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                             "Access-Control-Allow-Origin": "*",
                             "Access-Control-Allow-Headers": "session-id,Content-Type",
                             "Access-Control-Max-Age":86400,
                             "Content-Type":"application/json"})
    return response


def main(argv):
    
    Config.load(argv)
    LogWriter.setup()

    #setup graphyte for grafana metrics
    if Config.graphite_addr:
        graphyte.init(Config.graphite_addr,port=int(Config.graphite_port), prefix=socket.gethostname(), interval=10)
    
    #setup local cache
    file_storage.setup()

    #jobs
    #exampleJobWorker = threading.Thread(target=example_job.example_job)
    #exampleJobWorker.start()  

    LogWriter.info("API_SERVER_START")
        
    try:
        hostAddr = '0.0.0.0'
        app.run(host=hostAddr, port=Config.port, workers=Config.workers)
    except KeyboardInterrupt:
        print("quit")
    except:
        traceback.print_exc()
        
    print("quit again")
        
    jobs_mgr.do_stop = True
    #print("stopping example_job")
    #exampleJobWorker.join()


if __name__ == '__main__':
    main(sys.argv[1:])
