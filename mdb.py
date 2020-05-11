import pymongo

from utils.config import Config

# can throw
class mdb:

    client = None
    db = None


    @classmethod
    def reconnect(cls):
        uri = ""
        
        if Config.db_user and Config.db_passwd:
            uri = "mongodb://" + Config.db_user + ":" + Config.db_passwd + "@" + Config.db_addr + "?readPreference=primary"
        else:
            uri = "mongodb://" + Config.db_addr + "?readPreference=primary"


        #if not Config.is_test_system:
        #    uri = uri + "&ssl=true&ssl_ca_certs=" + Config.db_ca

        print("MONGO URI:" + uri)

        cls.client = pymongo.MongoClient(uri)

        if Config.is_test_system:
            cls.db = cls.client['vocab_test']
        else:
            cls.db = cls.client['vocab']


    @classmethod
    def getDB(cls):

        if not cls.client or not cls.db:
            cls.reconnect()

        if cls.client:
            cls.client.server_info()


    @classmethod     
    def any(cls, name):
        cls.getDB()
        return cls.db[name]
    
    @classmethod
    def config(cls):
        cls.getDB()
        return cls.db['config']
    
    @classmethod
    def user(cls):
        cls.getDB()
        return cls.db['user']

    @classmethod
    def user_sessions(cls):
        cls.getDB()
        return cls.db['user_sessions']

    
class dbns:

    class config:
        sendgrid_api_key = "sendgrid_api_key"
    
    class user:
        user_id = "user_id"
        email = "email"
        email_confirmed = "email_confirmed"
        password = "password"
        created = "created"
        modified = "modified"
        lastlogin = "lastlogin"
        lastname = "lastname"
        firstname = "firstname"
        accept_tos = "accept_tos"
        accept_data = "accept_data"
            

    class user_sessions:
        user_id = "user_id"
        session_id = "session_id"
        valid_until = "valid_until"
