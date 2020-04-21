from pymongo import MongoClient
from os import urandom
import time

from authconfig import MONGO_HOST, MONGO_PORT, ACCESS_TTL, REFRESH_TTL

ACCESS_TTL = 15
REFRESH_TTL = 50

class DataBase:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.db
        self.table = self.db.users

    def signup(self, doc):
        login = doc['login']
        if (self.exists(login)):
            raise Exception('User with login {} ALREADY EXISTS'.format(login))
        self.table.insert_one(doc)

    def signin(self, doc):
        login = doc['login']
        if (not self.exists(login)):
            raise Exception('Wrong login or password'.format(login))
        user = self.table.find_one({'login': login})
        if (user['password'] != doc['password']):
            raise Exception('Wrong login or password'.format(login))

        access_token = urandom(32).hex()
        refresh_token = urandom(32).hex()
        self.table.update_one({'login': login}, {'$set': {'access_token': access_token, 'refresh_token': refresh_token,
                                                          'time': int(round(time.time()))}})
        return {'access_token': access_token, 'refresh_token': refresh_token}


    def validate(self, doc):
        access_token = doc['access_token']
        user = self.table.find_one({'access_token': access_token})
        if (not user):
            return {'result' : False, 'details': 'Invalid access token'}
        cur_time = int(round(time.time()))
        if (cur_time - user['time'] > ACCESS_TTL):
            return {'result': False, 'details': 'Access token expired'}
        return {'result': True, 'details': 'Access token expired'}

    def refresh(self, doc):
        token = doc['refresh_token']
        user = self.table.find_one({'refresh_token': token})

        if (not user):
            return {'result' : False, 'details': 'Invalid refresh token'}
        cur_time = int(round(time.time()))
        if (cur_time - user['time'] > REFRESH_TTL):
            return {'result': False, 'details': 'Refresh token expired'}

        access_token = urandom(32).hex()
        refresh_token = urandom(32).hex()
        self.table.update_one({'refresh_token': token}, {'$set': {'access_token': access_token, 'refresh_token': refresh_token,
                                                                  'time': int(round(time.time()))}})


        return {"result" : True, 'details': {'access_token': access_token, 'refresh_token': refresh_token}}


    def exists(self, login):
        print("priv")
        if self.table.find({'login': login}).count() > 0:
            print("priv1")
            return True
        else:
            print("priv2")
            return False
