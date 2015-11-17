import os, uuid, app, hashlib
from app.database.db_connection import user_collection
import json, uuid, binascii
from bson import json_util
from flask.ext.mail import Message

class User():
    def __init__(self, o_id = None, token = None):
        if(o_id != None):
            mongo_user = user_collection.find_one({'_id': o_id})
        else:
            mongo_user = user_collection.find_one({'token': token})
        self.o_id = o_id
        self.f_name = mongo_user['firstname'] 
        self.l_name = mongo_user['lastname']
        self.email = mongo_user['email']
        self.password = mongo_user['password']
        self.token = mongo_user['token']
        self.tokenTTL = mongo_user['tokenTTL'] # update time to live
        self.is_auth = mongo_user['is_auth']
        self.events = json.loads(mongo_user['events'])
        self.roles = json.loads(mongo_user['roles'])
        self.year = mongo_user['year']
        self.major = mongo_user['major']
        self.skills = mongo_user['skills']
        self.dimensions = mongo_user['dimensions']
        
    def __init__(self, firstname, lastname, email, password, year, major):
        self.f_name = firstname 
        self.l_name = lastname
        self.email = email
        self.password = password
        self.token = User.gen_token()
        self.tokenTTL = 50 #this number is increased when account is authorized
        self.is_auth = False
        self.roles = User.get_role(email)
        self.events = []
        self.year = year
        self.major = major
        self.skills = []
        self.dimensions = []
            
        
    def json_dump(self):
        json_dict = {
            'firstname': self.f_name,
            'lastname': self.l_name,
            'email': self.email,
            'password': self.password,
            'token': self.token,
            'tokenTTL': self.tokenTTL,
            'is_auth': self.is_auth,
            'events': self.events,
            'roles': self.roles,
            'year': self.year,
            'major': self.major,
            'skills': self.skills,
            'dimensions': self.dimensions
        }
        return json_dict
        
    def is_authorized(self):
        return self.is_auth
    
    def send_verify(self, o_id):
        hash_token = str(hashlib.pbkdf2_hmac('sha256', self.token, b'salt', 100000))
        msg = Message("{0}/users/verifyUser/{1}/{2}".format(app.app.config['SERVER_NAME'], o_id, hash_token),
              sender="do.not.reply@gats-northeastern.com",
              recipients=[self.email])
        app.mail.send(msg)
    
    def update_ttl(self):
        user_collection.result = user_collection.update_one(
            {'_id': self.o_id},
            {'$set': {'tokenTTL': (self.tokenTTL - 1)}})        
    
    @staticmethod
    def gen_token():
        return str(uuid.uuid1())
    
    @staticmethod
    def authorize(o_id, token):
        tmp_user = user_collection.find_one({'_id': self.o_id})
        hash_token = hashlib.pbkdf2_hmac('sha256', tmp_user['token'], b'salt', 100000)
        if token == hash_token:
            user_collection.result = user_collection.update_one(
                {'_id': self.o_id},
                {
                    '$set': {'is_auth': True},
                    '$set': {'tokenTTL': 500} #increase as nesseceary
                })
            return True
        else:
            return False
        
    @staticmethod
    def get_role(email):
        if 'husky.neu.edu' in email:
            return ['student']
        elif 'northeastern.edu' in email or 'neu.edu' in email:
            return ['faculty']
        else:
            return 'Error'