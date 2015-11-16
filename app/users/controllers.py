from app.database.db_connection import user_collection
import json
from bson import json_util
from flask import Blueprint, request, jsonify
from cerberus import Validator
from app.users.user_model import User

users = Blueprint('users', __name__, url_prefix='/users')

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
        'regex': '^[a-zA-Z0-9_.+-]+@northeastern\.edu|neu\.edu|husky\.neu\.edu',
        'required': True,
        'unique': True
    },
    'password': {
        'type': 'string',
        'minlength': 8,
        'maxlength': 50
    },
    'token': {
        'type': 'string',
        'required': True,
        'unique': True
    },
    'tokenTTL': {
        'type': 'integer',
        'required': True
    },
    'is_auth': {
        type: 'boolean',
        'required': True
    },
    'events': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'Events',
            }
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
            'data_relation': {
                'resource': 'Skills',
            }
        }
    },
    'dimensions': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'Dimensions',
            }
        }
    }
}

schemaValidator = Validator(schema)

@users.route('/addUser', methods=['POST'])
def add_user():
    print data
    data = json.loads(request.data)
    if schemaValidator.validate(data):
        user = User.create_user(data['firstname'], data['lastname'],
                                   data['email'], password['year'], major['major'])
        if user != None:
            return json.dump({
                'response': {
                    'code': 200,
                    'msg': 'Success'
                },
                'user': {
                    'user_oid': user.o_id,
                    'token': user.token,
                }
            })
        return "ERROR: Could not add user. Please try again"
    return jsonify(schemaValidator.errors)

@users.route('/verifyUser/<o_id>/<token>')
def verify_user():
    if User.authorize(o_id, token):
        return "Success"
    else:
        return "ERROR: Could not authorize user. Please try again"

@users.route('/getUser/id/<auth_token>/<email>', methods=['GET'])
def get_user():
    all_events = list(user_collection.find({}, {"_id": 0}))
    return jsonify({"events": all_events})




