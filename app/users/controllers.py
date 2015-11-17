from app.database.db_connection import user_collection as usersdb
from app.database.db_connection import event_collection as events
from app.database.db_connection import dimension_collection as dimensions
from app.database.db_connection import skill_collection as skills
import json
from bson import json_util
from flask import Blueprint, request, jsonify
from app.users.user_model import User
from app.utils.validators import MyValidator

users = Blueprint('users', __name__, url_prefix='/users')

def validate_objectid(field, value, error, db):
    if not re.match('[a-f0-9]{24}', value) and db.find_one({'_id': value}):
        error(field, ERROR_BAD_TYPE.format('ObjectId'))

#validator for unique type
def validate_unique(field, value, error, db, search):
    if db.find_one({search: value}):
        error(field, "value '%s' is not unique" % value)
        
validate_email = lambda field, value, error: validate_unique(field, value, error, usersdb, 'email')
validate_token = lambda field, value, error: validate_unique(field, value, error, usersdb, 'token')
validate_event = lambda field, value, error: validate_objectid(field, value, error, events)
validate_skill = lambda field, value, error: validate_objectid(field, value, error, skills)
validate_dimension = lambda field, value, error: validate_objectid(field, value, error, dimensions)

    
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
        'type': 'string',
        'minlength': 8,
        'maxlength': 50
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
        #admins can do anything, superusers can't edit student and faculty accounts at will
        'allowed': ['student', 'faculty', 'superuser', 'admin']
    },
    'year': {
        'type': 'string',
        'allowed': ['Freshman', 'Sophomore', 'Middler', 'Junior', 'Senior']
    },
    'major': {
        'type': 'string',
        'maxlength': 50    
    },
    'skills': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'validator': validate_skill
            
        }
    },
    'dimensions': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'validator': validate_dimension,
        }
    }
}

schemaValidator = MyValidator(schema)

@users.route('/addUser', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    user = None
    try:
        user = User(data['firstname'], data['lastname'],
                           data['email'], data['password'],
                            data['year'], data['major'])
    except Exception as e:
        print e
        return json.dumps({ 'code': 400, 'msg': 'Fail'})
    
    data = user.json_dump()
    if schemaValidator.validate(data):
        o_id = usersdb.insert_one(data).inserted_id
        user.send_verify(o_id)
        return json.dumps({
            'response': {
                'code': 200,
                'msg': 'Success'
            },
            'user': {
                'user_oid': str(o_id),
                'token': user.token,
            }
        })
    return jsonify(schemaValidator.errors)

@users.route('/verifyUser/<o_id>/<token>')
def verify_user(o_id, token):
    if User.authorize(o_id, token):
        return "Success"
    else:
        return "ERROR: Could not authorize user. Please try again"

#@users.route('/getUser/id/<id>/<auth_token>/', methods=['GET'])    #add later if needed
@users.route('/getUser/em/<email>/<auth_token>/', methods=['GET'])
def get_user(email, auth_token):
    requester = User.get_user_from_db(token = auth_token)
    requested_user = User.get_user_from_db(email = email)
    if(requester.email == email or 'admin' in requester.roles):
        return requested_user.json_dump()
    else:
        return "Error: Permision Denied"




