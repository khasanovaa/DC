from pymongo import MongoClient
from os import urandom
import time
import json

from authconfig import MONGO_HOST, MONGO_PORT, ACCESS_TTL, REFRESH_TTL

class DataBase:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        # self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.db
        self.table = self.db.users

    def signup(self, doc):
        login = doc['login']
        if (self.exists(login)):
            user = self.table.find_one({'login': login})
            if (user['confirmed']):
                raise Exception('User with login {} ALREADY EXISTS'.format(login))
            else:
                return False
        self.table.insert_one(doc)
        self.table.update_one({'login': login},
                              {'$set': {'confirmed': False}})
        return True

    def signin(self, doc):
        login = doc['login']
        if (not self.exists(login)):
            raise Exception('Wrong login or password'.format(login))
        user = self.table.find_one({'login': login})
        if (user['password'] != doc['password']):
            raise Exception('Wrong login or password'.format(login))
        if (not user['confirmed']):
            raise Exception('Email is not confirmed')
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
        self.table.drop()
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


    def confirm(self, doc):
        token = doc['token']
        user = self.table.find_one({'token': token})
        if (not user):
            return {'result' : False, 'details': 'Invalid token'}
        user['confirmed'] = True
        self.table.update_one({'token': token},
                              {'$set': {'confirmed': True }})
        return {"result" : True, 'details': 'Email confirmed'}

    def addtoken(self, doc):
        token = doc['token']
        login = doc['login']
        user = self.table.find_one({'login': login})
        self.table.update_one({'login': login},
                              {'$set': {'token': token }})
        return True

    def exists(self, login):
        if self.table.find({'login': login}).count() > 0:
            return True
        else:
            return False
