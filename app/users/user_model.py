import os, uuid, app, hashlib, base64
from app.database.db_connection import user_collection
import json, uuid, binascii
from bson import json_util
from flask.ext.mail import Message

class User():
    def __init__(self, firstname, lastname, email, password, year, major, o_id = None):
        self.o_id = None
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
        hash_token = User.gen_hash(self.token)
        msg = Message("http://{0}/users/verifyUser/{1}/{2}".format(app.app.config['HOST'], o_id, hash_token),
              sender=('GATS', app.app.config['MAIL_USERNAME']),
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
    def gen_hash(token):
        #creates a url safe hash token
        return base64.urlsafe_b64encode(hashlib.md5(token).digest())[:11]
    
    @staticmethod
    def authorize(o_id, token):
        tmp_user = User.get_user_from_db(o_id = o_id)
        hash_token = User.gen_hash(token)
        if User.get_hash(tmp_user.token) == hash_token:
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
        
    @staticmethod
    def get_user_from_db(o_id = None, token = None, email = None):
        if(o_id != None):
            mongo_user = user_collection.find_one({'_id': o_id})
        elif token != None:
            mongo_user = user_collection.find_one({'token': token})
        else:
            mongo_user = user_collection.find_one({'email': email})
        return User(mongo_user['firstname'],
                    mongo_user['lastname'],
                    mongo_user['email'],
                    mongo_user['password'],
                    mongo_user['token'],
                    mongo_user['tokenTTL'], # update time to live
                    mongo_user['is_auth'],
                    json.loads(mongo_user['events']),
                    json.loads(mongo_user['roles']),
                    mongo_user['year'],
                    mongo_user['major'],
                    mongo_user['skills'],
                    mongo_user['dimensions'],
                    mongo_user['_id'])