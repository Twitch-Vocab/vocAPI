from typing import Dict
import os


import argparse

class Config:

    #testing
    is_test_system = True
    is_test = False
        
    #connection
    workers = 100
    port=443

    #mongo
    db_user = ""
    db_passwd = ""
    db_addr = ""

    #monitoring
    graylog_enable = False
    graylog_addr = ""
    graylog_port = 0
    graphite_enable = False
    graphite_addr = ""
    graphite_port = 0

    #temp files
    temp_file_path = ""
    

    @classmethod
    def load(cls, arg: Dict[str, str] = None, path = None):
        
        configFilePath = path

        # process command line args
        if not cls.is_test:
            parser = argparse.ArgumentParser()
            parser.add_argument("--config", help="force a config path", default="")
            args = parser.parse_args()
            
            if args.config: 
                configFilePath = args.config

        #get the configuration file path
        if not configFilePath:
            try:
                configFilePath = open("config_path", 'r').read().rstrip("\n\r")
            except FileNotFoundError:
                print("WARN: using fallback config path /home/ubuntu/config")
                configFilePath = "/home/ubuntu/config"
                
        print("load config from: " + configFilePath)
                   
        config_values = {}
        with open(configFilePath, 'r') as confFile:
            confFileLines = confFile.readlines()
            for line in confFileLines:
                if len(line.split("=")) == 2:
                    config_values.update({line.split("=")[0].rstrip("\n\r"): line.split("=")[1].rstrip("\n\r")})
                else:
                    print("WARN ERROR READING LINE: " + line)
            
        #process config file values
        #testing
        cls.is_test_system = config_values.get("is_test_system","no") in ["yes", "y", "true", "1"]

        #mongo
        cls.db_user = config_values["db_user"]
        cls.db_passwd = config_values["db_passwd"]
        cls.db_addr = config_values["db_addr"]
                
        #module configuration with default values for standard server
        cls.workers = int(config_values.get("workers", "100"))
        cls.port = int(config_values.get("port", "443"))

        #monitoring
        cls.graylog_enable = config_values.get("graylog_enable","false") in ["yes", "y", "true", "1"]
        cls.graylog_addr = config_values.get("graylog_addr", "")
        cls.graylog_port = int(config_values.get("graylog_port", "0"))
        cls.graphite_enable = config_values.get("graphite_enable","false") in ["yes", "y", "true", "1"]
        cls.graphite_addr = config_values.get("graphite_addr", "")
        cls.graphite_port = int(config_values.get("graphite_port", "0"))

        #temp files
        cls.temp_file_path = config_values.get("temp_file_path", "temp/")
        

        print("Config:")

        #testing
        print("is_test_system: " + str(cls.is_test_system))

        #connection
        print("workers: " + str(cls.workers))
        print("port: " + str(cls.port))

        #mongo
        print("db_user: " + str(cls.db_user))
        print("db_passwd: " + str(len(cls.db_user)))
        print("db_addr: " + str(cls.db_addr))

        #monitoring
        print("graylog_enable: " + str(cls.graylog_enable))
        print("graylog_addr: " + str(cls.graylog_addr))
        print("graylog_port: " + str(cls.graylog_port))
        print("graphite_enable: " + str(cls.graphite_enable))
        print("graphite_addr: " + str(cls.graphite_addr))
        print("graphite_port: " + str(cls.graphite_port))

        #local file cache
        print("temp_file_path: " + str(cls.temp_file_path))
