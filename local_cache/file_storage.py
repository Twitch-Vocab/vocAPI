from typing import Dict, Tuple, List
import time
import traceback
import time
import os

#UTILS
from utils.config import Config
from utils.graylog import LogWriter


def setup():
    try:
        os.mkdir(Config.temp_file_path)
    except FileExistsError:
        return
    except:
        traceback.print_exc()
        LogWriter.alert("local_cache_setup_failed")


def get_temp_file_path(file_id:str) -> str:
    
    if not file_id:
        return False
    
    file_path = Config.temp_file_path
    if not file_path:
        LogWriter.alert("no_temp_file_path")
        return False
           
    return file_path + "/" + file_id


#add data to a temporary file
def append_temp_file(file_id: str, data: bytes) -> bool:
    result = False

    try:
        if not file_id:
            return False
    
        file_path = get_temp_file_path(file_id)

        with open(file_path, 'ab+') as temp_file:
            temp_file.write(data)
            result = True
    except:
        traceback.print_exc()
    
    return result


def get_temp_file(file_id: str) -> bytes:
    data = None

    try:
        file_path = get_temp_file_path(file_id)

        if not os.path.isfile(file_path):
            return data
    
        with open(file_path, 'rb+') as temp_file:
            data = temp_file.read()
    except:
        traceback.print_exc()
    return data


def remove_temp_file(file_id: str):
    try:
        if not exists(file_id):
            return

        file_path = get_temp_file_path(file_id)

        os.remove(file_path)

        #return not exists(file_path)
    except:
        traceback.print_exc()



def exists(file_id: str) -> bool:
    file_path = get_temp_file_path(file_id)

    return os.path.isfile(file_path)


def size(file_id: str) -> int:
    if not exists(file_id):
        return -1
    
    file_path = get_temp_file_path(file_id)

    size = os.path.getsize(file_path)

    return size


def set_modified_now(file_id: str):
    try:
        file_path = get_temp_file_path(file_id)

        if not os.path.isfile(file_path):
            return

        os.utime(file_path)

    except:
        traceback.print_exc()
        

def cleanup():
    #print("LOCAL_CACHE CLEANUP")
    temp_file_path = Config.temp_file_path

    now = int(time.time())
    for one_filename in os.listdir(temp_file_path):
        
        file_path = temp_file_path + "/" + one_filename
        modified_at = int(os.path.getmtime(file_path))
        #print("CHECK " + one_filename + " AGE: " + str(now - modified_at))
        if(now - modified_at > 24*3600):
            print("LOCAL_CACHE DELETE " + one_filename)
            os.remove(file_path)