from app.database.mongo import event_collection, skill_collection
import json
from bson import json_util
from flask import Blueprint, request
from cerberus import Validator
import datetime

events = Blueprint('events', __name__, url_prefix='/events')


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
    'title': {
        'required': True,
        'type': 'string',
        'validator': validate_title_does_not_exist
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
        'type': 'string',
        'validator': validate_date
    },
    'end': {
        'required': True,
        'type': 'string',
        'validator': validate_date
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
            'number': {'type': 'string', 'validator': validate_phone_number},
            'email': {'type': 'string', 'validator': validate_email}
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
    }
    # 'owner': {
    #         'type': 'string',
    #         'required': True,
    #         # referential integrity constraint: value must exist in the
    #         # 'people' collection. Since we aren't declaring a 'field' key,
    #         # will default to `people._id` (or, more precisely, to whatever
    #         # ID_FIELD value is).
    #         'data_relation': {
    #             'resource': 'users',
    #             # make the owner embeddable with ?embedded={"owner":1}
    #             'embeddable': True
    #         },
    # }
}

schemaValidator = Validator(schema)


@events.route('/addEvent', methods=['POST'])
def add_event():
    data = json.loads(request.data)
    if schemaValidator.validate(data):
        mongo_id = event_collection.insert_one(data).inserted_id
        if mongo_id:
            return "Success"
        return "ERROR: Could not create event. Please try again"
    return json.dumps(schemaValidator.errors)


@events.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = event_collection.find({}, {"_id": 0})
    events_from_db = [json.dumps(e, default=json_util.default) for e in all_events]
    return json.dumps(events_from_db)
