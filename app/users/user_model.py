import uuid, hashlib, binascii, base64, app
from app.database.db_connection import user_collection, skill_collection, dimension_collection
from bson import ObjectId
from flask.ext.sendmail import Message

# user class for all users in the system
class User:
   
    DEFAULT_TTL = 500

    # constructor to create a user
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
        if len(roles) == 0:
            self.roles = User.get_role(email)
        else:
            self.roles = roles
        self.events = events
        self.year = year
        self.major = major
        if len(skills) == 0:
            # pulls skills from DB and assign them to the user
            self.skills = User.set_skills()
        else:
            self.skills = skills
        if len(dimensions) == 0:
            # pull the dimensions from the DB and assign them to the user
            self.dimensions = User.set_dimensions()
        else:
            self.dimensions = dimensions

    @staticmethod
    # set the skills from the DB on the user
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
    # set the dimensions from the DB on the user
    def set_dimensions():
        dimensions = list(dimension_collection.find({}))
        dimension_to_points = []
        for dimension in dimensions:
            dimension_dict = {}
            dimension_dict['dimension'] = dimension['name']
            dimension_dict['value'] = 0
            dimension_to_points.append(dimension_dict)
        return dimension_to_points

    # creates a JSON dump of the
    def json_dump(self, inc_pass=False):
        if inc_pass:
            pwd = self.password
        else:
            pwd = ''
        json_dict = {
            'firstname': self.f_name,
            'lastname': self.l_name,
            'email': self.email,
            'password': pwd,
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

    # returns if a user has a certain role
    def can_access(self, email):
        return 'admin' in self.roles or ('faculty' in self.roles and 'student' in User.get_role(email))

    # returns if a user is authorized (verified email)
    def is_authorized(self):
        return self.is_auth

    # send the verification email to the user
    def send_verify(self, o_id):
        hash_token = User.gen_token_hash(self.token)
        html_body = "Please verify your account by clicking the link below!<br>"
        msg_body = "<a href='http://{0}:{1}/users/verifyUser/{2}/{3}'>Click Here!</a><br><br>".format(app.app.config['HOST'],
                                                                   app.app.config['PORT'],
                                                                   o_id, hash_token)
        rest = "If the link above does not work, copy and paste the following link into your browser:<br>"\
            "http://{0}:{1}/users/verifyUser/{2}/{3}'".format(app.app.config['HOST'],
                                                                   app.app.config['PORT'],
                                                                   o_id, hash_token)
        msg = Message("Verfy with GATS",
                      sender=('GATS', app.app.config['MAIL_USERNAME']),
                      recipients=[self.email])
        msg.html = html_body + msg_body + rest
        if not app.app.config['TESTING']:
            app.mail.send(msg)

    # decrements the TTL for the token
    def update_ttl(self):
        user_collection.result = user_collection.update_one(
            {'_id': self.o_id},
            {'$set': {'tokenTTL': (self.tokenTTL - 1)}})        
    
    # updates token ttl and produces a new token if this one expires
    def update_token(self):
        if self.tokenTTL is 0:
            self.token = User.gen_token()
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(self.o_id)},
                {
                    '$set': {'token': self.token, 'tokenTTL': User.DEFAULT_TTL}  # increase as necessary
                })
        else:
            self.update_ttl()

    # generates a unique token
    @staticmethod
    def gen_token():
        return str(uuid.uuid1())

    # generates a password hash
    @staticmethod
    def gen_pw_hash(password, sugar):
        # TODO make salt more unique
        salt = app.app.config['SALT'] + sugar
        return hashlib.sha512(password + salt).hexdigest()

    # generates a token hash
    @staticmethod
    def gen_token_hash(token):
        # creates a url safe hash token
        return base64.urlsafe_b64encode(hashlib.md5(token).digest())[:11]

    # authorizes a user - triggered from verification email
    @staticmethod
    def authorize(o_id, token):
        tmp_user = User.get_user_from_db(o_id = o_id)
        tmp_user_token = User.gen_token_hash(tmp_user.token)
        if tmp_user_token == token:
            user_collection.result = user_collection.update_one(
                {'_id': ObjectId(o_id)},
                {
                    '$set': {'is_auth': True, 'tokenTTL': User.DEFAULT_TTL}  # increase as nesseceary
                })
            return True
        else:
            return False

    # returns roles based on the email address
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

    # gets a user from the database based on one of the input fields
    @staticmethod
    def get_user_from_db(o_id=None, token=None, email=None, is_post=False):
        if token is not None:
            mongo_user = user_collection.find_one({'token': token})
        elif o_id is not None:
            mongo_user = user_collection.find_one({'_id': ObjectId(o_id)})
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
        if is_post:
            user.update_token()
        return user

    # returns a user if they are authorized for the role
    @staticmethod
    def get_user_check_auth(role, token, is_post=False):
        user = User.get_user_from_db(token=token, is_post=is_post)
        if user is not None:
            if role in user.roles:
                return user
        return None
    
    # returns a user if they are authorized to get that user
    @staticmethod
    def get_user_if_auth(o_id=None, token=None, email=None, password=None, is_post=False):
        user = User.get_user_from_db(o_id, token, email)
        if user is not None:
            if token is not None:
                if email != user.email:
                    if user.can_access(email):
                        return user
                else:
                    return user
            else:
                if user.password == User.gen_pw_hash(password, user.email):
                    return user
        return None
