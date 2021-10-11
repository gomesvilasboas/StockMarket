import pymongo
import logging
from threading import Lock
import time
import json
import os

class MongoDB:

    logging.basicConfig(filename='./log/MongoDB.log', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger_lock = Lock()

    def __init__(self):
        self.LoadConfig()
    
    def LoadConfig(self):
        with open('./config/MongoDB.config') as jsonfile:
            config = json.load(jsonfile)
            self.__databaseName = config['DatabaseName']
            self.__URI = config['URI']

    
    def Initalize(self):
        user =  os.getenv('MongoDBUSer')
        passwd = os.getenv('MongoDBPasswd')
        client = pymongo.MongoClient(self.__URI, user = user, password = passwd)
        self.__database = client[self.__databaseName]
    
    def Insert(self, collection, data):
        try:
            self.__database[collection].insert(data)
            msg = '[{timestamp}] Data inserted'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
            logging.info(msg)
            return True
        except Exception as ex:
            msg = '[{timestamp}] Error: {error}'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), error=str(ex))
            logging.error(msg)
            return False

    def Find(self, collection, query):
        try:
            return self.__database[collection].find(query)
        except Exception as ex:
            msg = '[{timestamp}] Error: {error}'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), error=str(ex))
            logging.info(msg)
            return None

    def FindOne(self, collection, query):
        try:
            return self.__database[collection].find_one(query)
        except Exception as ex:
            msg = '[{timestamp}] Error: {error}'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), error=str(ex))
            logging.error(msg)
            return None
    
    def Delete(self, collection, query):
        try:
            self.__database[collection].delete_one(query)
            msg = '[{timestamp}] Data deleted'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
            logging.info(msg)
            return True
        except Exception as ex:
            msg = '[{timestamp}] Error: {error}'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), error=str(ex))
            logging.error(msg)
            return False