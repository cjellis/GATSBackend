from app.database.mongo import event_collection, skill_collection
import json
from bson import json_util
# Import flask dependencies
from flask import Blueprint, request
from cerberus import Validator
# Define the blueprint: 'auth', set its url prefix: app.url/auth
events = Blueprint('events', __name__, url_prefix='/events')


def validate_skills_exist(field, value, error):
    for v in value:
        if skill_collection.find({"name": v}).count() is 0:
            error(field, "Skill does not exist")


schema = {
    'title': {
        'required': True,
        'type': 'string'
    },
    'format': {
        'required': True,
        'type': 'string'
    },
    'topics': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    },
    'description': {
        'required': True,
        'type': 'string'
    },
    'begin': {
        'required': True,
        'type': 'string'
    },
    'end': {
        'required': True,
        'type': 'string'
    },
    'engagementLengthValue': {
        'required': True,
        'type': 'integer'
    },
    'engagementLengthUnit': {
        'required': True,
        'type': 'string',
        'allowed': ['Day', 'Week', 'Month', 'Semester', 'Year']
    },
    'recurrence': {
        'required': True,
        'type': 'string'
    },
    'location': {
        'required': True,
        'type': 'string'
    },
    'sponsoringDepartment': {
        'required': True,
        'type': 'string'
    },
    'pointOfContact': {
        'required': True,
        'type': 'dict',
        'schema': {
            'name': {'type': 'string'},
            'number': {'type': 'string'},
            'email': {'type': 'string'}
        }
    },
    'outcomes': {
        'required': True,
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'skills': {
        'required': True,
        'type': 'list',
        'schema': {'type': 'string'},
        'validator': validate_skills_exist
    },
    'engagementLevel': {
        'required': True,
        'type': 'string',
        'allowed': ['Active', 'Passive', 'Generative']
    },

    'coopFriendly': {
        'type': 'boolean'
    },
    'academicStanding': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'major': {
        'type': 'string'
    },
    'residentStatus': {
        'type': 'string',
        'allowed': ['onCampus', 'offCampus', 'both']
    },
    'otherRequirements': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'users',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
}

schemaValidator = Validator(schema)


@events.route('/addEvent', methods=['POST'])
def add_event():
    data = json.loads(request.data)
    if schemaValidator.validate(data):
        if event_collection.find({"title": data["title"]}).count() is 0:
            mongo_id = event_collection.insert_one(data).inserted_id
            if mongo_id:
                return "Success"
            return "ERROR: Could not create event. Please try again"
        return "ERROR: Event Exists with that Title"
    return json.dumps(schemaValidator.errors)


@events.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = event_collection.find()
    events_from_db = [json.dumps(e, default=json_util.default) for e in all_events]
    return json.dumps(events_from_db)
