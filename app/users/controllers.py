from app.database.mongo import user_collection
import json
from bson import json_util
from flask import Blueprint, request, jsonify
from cerberus import Validator

users = Blueprint('users', __name__, url_prefix='/users')


def validate_skills_exist(field, value, error):
    for v in value:
        if skill_collection.find({"name": v}).count() is 0:
            error(field, "Skill does not exist - " + v)


def validate_title_does_not_exist(field, value, error):
    if event_collection.find({"title": value}).count() is not 0:
        error(field, "Event already exists with given title")


def validate_date(field, value, error):
    try:
        datetime.datetime.strptime(value, '%m/%d/%Y')
    except ValueError:
        error(field, "Date not in correct format")


def validate_phone_number(field, value, error):
    if len(value) is not 10:
        error(field, "Phone Number not long enough")


def validate_email(field, value, error):
    if not value.endswith("@neu.edu"):
        error(field, "Email is not an @neu email")


schema = {
    # 'title' tag used in item links.
    'item_title': 'user',
    'internal_resource': False,
    'resource_title': 'user',

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'schema': {
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
        }
        
        'events': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'events',
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
                    'resource': 'skills',
                }
            }
        },
        'dimensions': {
            'type': 'list',
            'schema': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'dimensions',
                }
            }
        }
    }
}

schemaValidator = Validator(schema)

@users.route('/addUser', methods=['POST'])
def add_user():
    data = json.loads(request.data)
    if schemaValidator.validate(data):
        mongo_id = user_collection.insert_one(data).inserted_id
        if mongo_id:
            return "Success"
        return "ERROR: Could not user event. Please try again"
    return jsonify(schemaValidator.errors)


@users.route('/getUser/id/<auth_token>/<user_id>', methods=['GET'])
def get_user():
    all_events = list(event_collection.find({}, {"_id": 0}))
    return jsonify({"events": all_events})



#@app.route('/user/t/<auth_token>/<user_id>')
#@app.route('/user/p/<passwd>/<user_id>')
#def getUser(user_id, auth_token = None, passwd = None):
#    if passwd == None:
#        userData = "user tok" #UPDATE
#    else:
#        userData = "user pw" #update
#    updateTTL(userData)
#    return userData

#@app.route('/user/make', methods=['PUT'])
#def createUser():
#
#@app.route('/user/<auth_token>/<user_id>/update', methods['POST'])
#def updateUser():
# 


