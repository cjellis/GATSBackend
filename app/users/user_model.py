import uuid, hashlib, base64, app
from app.database.db_connection import user_collection, skill_collection, dimension_collection
from bson import ObjectId
from flask.ext.mail import Message


class User:
   
    DEFAULT_TTL = 500

    def __init__(self, firstname, lastname, email, 
                 password, year=None, major=None, token=None,
                 tokenTTL=50, is_auth=False,
                 roles=[], events=[], skills=[],
                 dimensions=[], o_id=None):
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
        self.tokenTTL = tokenTTL  # this number is increased when account is authorized
        self.is_auth = is_auth
        if roles is None:
            self.roles = User.get_role(email)
        else:
            self.roles = roles
        self.events = events
        self.year = year
        self.major = major
        if len(skills) == 0:
            self.skills = User.set_skills()
        else:
            self.skills = skills
        if len(dimensions) == 0:
            self.dimensions = User.set_dimensions()
        else:
            self.dimensions = dimensions

    @staticmethod
    def set_skills():
        skills = list(skill_collection.find({}))
        skill_to_points = []
        for skill in skills:
            skill_dict = {}
            skill_dict['skill'] = skill['name']
            skill_dict['value'] = 0
            skill_to_points.append(skill_dict)
        return skill_to_points

    @staticmethod
    def set_dimensions():
        dimensions = list(dimension_collection.find({}))
        dimension_to_points = []
        for dimension in dimensions:
            dimension_dict = {}
            dimension_dict['dimension'] = dimension['name']
            dimension_dict['value'] = 0
            dimension_to_points.append(dimension_dict)
        return dimension_to_points
        
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
        hash_token = User.gen_token_hash(self.token)
        msg_body = "http://{0}:{1}/users/verifyUser/{2}/{3}".format(app.app.config['HOST'],
                                                                   app.app.config['PORT'],
                                                                   o_id, hash_token)
        msg = Message("Verfy with GATS",
                      sender=('GATS', app.app.config['MAIL_USERNAME']),
                      recipients=[self.email])
        msg.body = msg_body
        if not app.app.config['TESTING']:
            app.mail.send(msg)
    
    def update_ttl(self):
        user_collection.result = user_collection.update_one(
            {'_id': self.o_id},
            {'$set': {'tokenTTL': (self.tokenTTL - 1)}})        
    
    # updates token ttl and produces a new token if this one expires
    def update_token(self):
        if self.tokenTTL is 0:
            self.token = User.gen_token()
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(o_id)},
                {
                    '$set': {'token': self.token, 'tokenTTL': DEFAULT_TTL}  # increase as necessary
                })
        else:
            self.update_ttl()
            
    # authorizes requests based on role
    def auth_request(self, role=None):
        return 'admin' in self.roles or role in self.roles
    
    
    @staticmethod
    def gen_token():
        return str(uuid.uuid1())
    
    @staticmethod
    def gen_pw_hash(password):
        #TODO make salt more unique
        salt = app.app.config['SALT']
        return hashlib.sha512(password).hexdigest()
    
    @staticmethod
    def gen_token_hash(token):
        # creates a url safe hash token
        return base64.urlsafe_b64encode(hashlib.md5(token).digest())[:11]
    
    @staticmethod
    def authorize(o_id, token):
        tmp_user = User.get_user_from_db(o_id = o_id)
        tmp_user_token = User.gen_token_hash(tmp_user.token)
        if tmp_user_token == token:
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(o_id)},
                {
                    '$set': {'is_auth': True, 'tokenTTL': DEFAULT_TTL}  # increase as nesseceary
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
        
    # fixes the exploit that allows users to repeatedly register with the same email account
    @staticmethod
    def fix_email_bug(email):
        if '+' in email:
            l = email.split('+')
            l2 = l[1].split('@')
            if len(l2) > 1:
                return l[0] + '@' + l2[1]
            else:
                return l[0] + l[1]
        else:
            return email
    
    @staticmethod
    def get_user_from_db(o_id=None, token=None, email=None, is_post=False):
        if o_id is not None:
            mongo_user = user_collection.find_one({'_id': ObjectId(o_id)})
        elif token is not None:
            mongo_user = user_collection.find_one({'token': token})
        else:
            mongo_user = user_collection.find_one({'email': email})
            
        if mongo_user is None:
            return None
        user = User(mongo_user['firstname'],
                    mongo_user['lastname'],
                    mongo_user['email'],
                    mongo_user['password'],
                    mongo_user['year'],
                    mongo_user['major'],
                    mongo_user['token'],
                    mongo_user['tokenTTL'],  # update time to live
                    mongo_user['is_auth'],
                    mongo_user['roles'],  # json.loads(mongo_user['roles']),
                    mongo_user['events'],  # json.loads(mongo_user['events']),
                    mongo_user['skills'],
                    mongo_user['dimensions'],
                    mongo_user['_id'])
        # will add back in later
        if is_post user.update_token()
        return user
    
    # returns a user if they are authorized for a role
    @staticmethod
    def get_user_if_auth(role, o_id=None, token=None, email=None, is_post=False):
        user = get_user_from_db(o_id, token, email)
        if user is not None:
            if user.auth_request(role):
                return user
        return None
    
    # returns weather a user is authorized for a role
    @staticmethod
    def get_user_is_auth(role, o_id=None, token=None, email=None, is_post=False):
        return get_user_if_auth(role, o_id, token, email) is None
        
