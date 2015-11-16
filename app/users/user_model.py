from app.database.mongo import user_collection
import json, uuid, binascii
from bson import json_util

class User():
    def __init__(self, o_id = None, token = None):
        if(o_id != None:):
            mongo_user = user_collection.find_one({'_id': o_id})
        else:
            mongo_user = user_collection.find_one({'token': token})
        self.o_id = o_id
        self.f_name = mongo_user['firstname'] 
        self.l_name = mongo_user['lastname']
        self.email = mongo_user['password']
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
        self.token = os.urandom(32)
        self.tokenTTL = 50 #this number is increased when account is authorized
        self.is_auth = False
        self.roles = roles
        self.events = []
        self.year = year
        self.major = major
        self.skills = []
        self.dimensions = []
        
    @staticmehtod
    def create_new_user(firstname, lastname, email, password, year, major):
        if 'husky.neu.edu' in email:
            user = User(firstname, lastname, email, ['Student'], password, year, major)
            user.o_id = user_collection.insert_one(user.json_dump()).inserted_id
            user.send_verify()
            return user
        elif 'northeastern.neu' in email or 'neu.edu' in email:
            user = User(firstname, lastname, email, ['Faculty'], password, None, None)
            user.o_id = user_collection.insert_one(user.json_dump()).inserted_id
            user.send_verify()
            return user
        else:
            None
        
    def json_dump(self):
        json_dict = {
            'firstname': f_name,
            'lastname': l_name,
            'email': email,
            'password': password,
            'tokenTTL': tokenTTL,
            'events': events,
            'roles': roles,
            'year': year,
            'major': major,
            'skills': skills,
            'dimensions': dimensions
        }
        
    def is_authorized(self):
        return is_auth
    
    def send_verify():
        return
    
    def update_ttl(self):
        user_collection.result = user_collection.update_one(
            {'_id': 'o_id'},
            {'$set': {'tokenTTL': (tokenTTL - 1)}})        
    
    @staticmehtod
    def authorize(o_id, token):
        tmp_user = user_collection.find_one({'_id': o_id})
        hash_token = hashlib.pbkdf2_hmac('sha256', tmp_user['token'], b'salt', 100000)
        if token == hash_token:
            user_collection.result = user_collection.update_one(
                {'_id': 'o_id'},
                {'$set': {'is_auth': True}})
            return True
        else:
            return False