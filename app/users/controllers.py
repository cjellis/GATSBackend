from app.database.db_connection import user_collection as usersdb
from app.database.db_connection import event_collection as events
from app.database.db_connection import dimension_collection as dimensions
from app.database.db_connection import skill_collection as skills
import json
from flask import Blueprint, request
from app.users.user_model import User
from app.utils.validators import MyValidator
from app.utils.msg_tools import ResponseTools as msg_tools

users = Blueprint('users', __name__, url_prefix='/users')


def validate_objectid(field, value, error, db):
    if not re.match('[a-f0-9]{24}', value) and db.find_one({'_id': ObjectId(value)}):
        error(field, ERROR_BAD_TYPE.format('ObjectId'))

# validator for unique type
def validate_unique(field, value, error, db, search):
    if db.find_one({search: value}):
        error(field, "value '%s' is not unique" % value)
        
validate_email = lambda field, value, error: validate_unique(field, value, error, usersdb, 'email')
validate_token = lambda field, value, error: validate_unique(field, value, error, usersdb, 'token')
validate_event = lambda field, value, error: validate_objectid(field, ObjectId(value), error, events)
validate_skill = lambda field, value, error: validate_objectid(field, ObjectId(value), error, skills)
validate_dimension = lambda field, value, error: validate_objectid(field, ObjectId(value), error, dimensions)

    
schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'firstname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 10,
        'required': True
    },
    'lastname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 15,
        'required': True
    },
    'email': {
        'type': 'string',
        'regex': '(^[a-zA-Z0-9_.+-]+@)(northeastern\.edu|neu\.edu|husky\.neu\.edu)',
        'required': True,
        'validator': validate_email
    },
    'password': {
        'type': 'string'
    },
    'token': {
        'type': 'string',
        'required': True,
        'validator': validate_token
    },
    'tokenTTL': {
        'type': 'integer',
        'required': True
    },
    'is_auth': {
        'type': 'boolean',
        'required': True
    },
    'events': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'validator': validate_event
        }
    },
    # 'role' is a list, and can only contain values from 'allowed'.
    'roles': {
        'type': 'list',
        # admins can do anything, superusers can't edit student and faculty accounts at will
        'allowed': ['student', 'faculty', 'superuser', 'admin']
    },
    'year': {
        'type': 'string',
        'nullable': True,
        'allowed': ['Freshman', 'Sophomore', 'Middler', 'Junior', 'Senior']
    },
    'major': {
        'type': 'string',
        'nullable': True,
        'maxlength': 50    
    },
    'skills': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'skill': {'type': 'string'},
                'value': {'type': 'integer'}
            }
        }
    },
    'dimensions': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'dimension': {'type': 'string'},
                'value': {'type': 'integer'}
            }
        }
    }
}

schemaValidator = MyValidator(schema)


@users.route('/addUser', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    email = data['email']
    email = User.fix_email_bug(email)
    # comment back in to do testing on a single address
    # email = data['email']

    if 'year' in data and 'major' in data:
        user = User(data['firstname'], data['lastname'], email,
                    data['password'], data['year'], data['major'])
    else:
        password = User.gen_pw_hash(data['password'])
        user = User(data['firstname'], data['lastname'], email,
                    password)
        
    data = user.json_dump()
    if schemaValidator.validate(data):
        o_id = usersdb.insert_one(data).inserted_id
        user.send_verify(o_id)
        return msg_tools.response_success(objects={'user': {'user_oid': str(user.email), 'token': user.token}})
    return msg_tools.response_fail(objects=schemaValidator.errors)


@users.route('/verifyUser/<o_id>/<token>', methods=['GET'])
def verify_user(o_id, token):
    if User.authorize(o_id, token):
        return msg_tools.response_success(msg="Successfully authorized you!")
    else:
        return msg_tools.response_fail(msg="We could not authorize you. Please try again")


# @users.route('/getUser/id/<id>/<auth_token>', methods=['GET'])    #add later if needed
@users.route('/getUser/em/<email>/<auth_token>', methods=['GET'])
def get_user(email, auth_token):
    requester = User.get_user_from_db(token=auth_token)
    requested_user = User.get_user_from_db(email=email)
    if requester.email == email or 'admin' in requester.roles:
        return msg_tools.response_success(objects=requested_user.json_dump())
    else:
        return msg_tools.response_fail(code=401, objects={'error': 'permission denied'})
