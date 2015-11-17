import os, uuid, hashlib, base64, app
from app.database.db_connection import user_collection
import json, uuid, binascii
from bson import json_util, ObjectId
from flask.ext.mail import Message

class User():
    def __init__(self, firstname, lastname, email, 
                 password, year, major, token = None,
                 tokenTTL = 50, is_auth = False, 
                 roles = None, events = [], skills = [],
                 dimensions = [], o_id = None):
        self.o_id = o_id
        self.f_name = firstname 
        self.l_name = lastname
        self.email = email
        self.password = password
        if token is None:
            token = User.gen_token()
        else:
            token = token
        self.token = token
        self.tokenTTL = tokenTTL #this number is increased when account is authorized
        self.is_auth = is_auth
        if roles is None:
            self.roles = User.get_role(email)
        else:
            self.roles = roles
        self.events = events
        self.year = year
        self.major = major
        self.skills = skills
        self.dimensions = dimensions
            
        
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
        msg_body ="http://{0}:{1}/users/verifyUser/{2}/{3}".format(app.app.config['HOST'], 
                                                                    app.app.config['PORT'],
                                                                       o_id, hash_token)
        msg = Message("Verfy with GATS",
              sender=('GATS', app.app.config['MAIL_USERNAME']),
              recipients=[self.email])
        msg.body = msg_body
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
        tmp_user_token = User.gen_hash(tmp_user.token)
        print tmp_user.email
        print tmp_user.token
        print tmp_user_token
        print token
        if tmp_user_token == token:
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(o_id)},
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
            mongo_user = user_collection.find_one({'_id': ObjectId(o_id)})
        elif token != None:
            mongo_user = user_collection.find_one({'token': token})
        else:
            mongo_user = user_collection.find_one({'email': email})
        return User(mongo_user['firstname'],
                    mongo_user['lastname'],
                    mongo_user['email'],
                    mongo_user['password'],
                    mongo_user['year'],
                    mongo_user['major'],
                    mongo_user['token'],
                    mongo_user['tokenTTL'], # update time to live
                    mongo_user['is_auth'],
                    mongo_user['roles'], #json.loads(mongo_user['roles']),
                    mongo_user['events'], #json.loads(mongo_user['events']),
                    mongo_user['skills'],
                    mongo_user['dimensions'],
                    mongo_user['_id'])