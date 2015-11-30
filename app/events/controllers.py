from app.database.db_connection import event_collection, skill_collection, user_collection
from app.users.user_model import User
from app.utils.msg_tools import ResponseTools as response
import json
from flask import Blueprint, request, jsonify
from cerberus import Validator
import datetime
import uuid

events = Blueprint('events', __name__, url_prefix='/events')

length_to_value_map = {
    'Day': 1,
    'Week': 2,
    'Month': 3,
    'Semester': 4,
    'Year': 5
}

level_to_value_map = {
    'Active': 1,
    'Passive': 2,
    'Generative': 3
}


# validator for unique type
def validate_unique(field, value, error, db, search):
    if db.find_one({search: value}):
        error(field, "value '%s' is not unique" % value)


def validate_id(field, value, error):
    validate_unique(field, value, error, event_collection, 'id')


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
    },
    'attendance': { #change to attendants?
        'type': 'list',
        'schema': {'type': 'string'}  # user email?
    },
    'id': {
        'type': 'string',
        'required': True,
        'validator': validate_id
    },
    'state': {
        'type': 'string',
        'allowed': ['open', 'over', 'closed', 'completed'],
        'required': True
    },
    'checkAttendance': {
        'type': 'boolean',
        'required': True
    },
    'owner': {
        'type': 'string',
        'required': True
    }
}

schemaValidator = Validator(schema)


@events.route('/addEvent/<auth_token>', methods=['POST'])
def add_event(auth_token):
    data = json.loads(request.data)
    data['id'] = str(uuid.uuid4())
    data['attendance'] = []
    data['state'] = 'open'
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to create an event")
    data['owner'] = user.email
    if schemaValidator.validate(data):
        mongo_id = event_collection.insert_one(data).inserted_id
        if mongo_id:
            return response.response_success()
        return response.response_fail(msg="ERROR: Could not create event. Please try again")
    return jsonify(schemaValidator.errors)


@events.route('/submitAttendance/<event_id>/<auth_token>', methods=['POST'])
def submit_attendance(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['state'] == 'closed' or event['state'] == 'completed':
        return response.response_fail(msg="ERROR: Event is already closed")
    attendance = event['attendance']
    attendance.append({"firstName": user.f_name, "lastName": user.l_name, "email": user.email})
    user.events.append(event_id)
    event_collection.update_one({"id": event_id}, {"$set": {"attendance": attendance}})
    user_collection.update_one({"email": user.email}, {"$set": {"events": user.events}})
    return response.response_success()


@events.route('/changeAttendance/<event_id>/<auth_token>', methods=['POST'])
def change_attendance(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")

    event_collection.update_one({"id": event_id}, {"$set": {"checkAttendance": not event['checkAttendance']}})
    return response.response_success()


@events.route('/getAttendance/<event_id>/<auth_token>', methods=['GET'])
def get_attendance(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")

    attendance = event['attendance']

    return jsonify({"attendees": attendance})


@events.route('/verifyAttendance/<event_id>/<auth_token>', methods=['POST'])
def verify_attendance(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'closed':
        return response.response_fail(msg="ERROR: Event not yet closed")
    if not event['checkAttendance']:
        return response.response_fail(msg="ERROR: attendance does not need to be verified")

    event_level = event['engagementLevel']
    level_value = level_to_value_map.get(event_level)
    event_length = event['engagementLengthUnit']
    length_value = length_to_value_map.get(event_length)
    event_length_value = event['engagementLengthValue']
    points_per_skill = length_value * event_length_value * level_value
    skills = event['skills']

    data = json.loads(request.data)
    attendees = data['attendees']
    for email in attendees:
        user = User.get_user_from_db(email=email)
        for skill in skills:
            for user_skill in user.skills:
                if user_skill['skill'] == skill:
                    user_skill['value'] += points_per_skill
                    skill_dimensions = list(skill_collection.find_one({"name": skill})['dimensions'])
                    for dimension in skill_dimensions:
                        for user_dimension in user.dimensions:
                            if user_dimension['dimension'] == dimension:
                                user_dimension['value'] += points_per_skill
                                break
            break
        user_collection.update_one({"email": email},
                                   {"$set":
                                    {'skills': user.skills, 'dimensions': user.dimensions}})
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'completed', 'attendance': attendees}})

    return response.response_success()


@events.route('/distributePoints/<event_id>/<auth_token>', methods=['POST'])
def distribute_points(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'closed':
        return response.response_fail(msg="ERROR: Event not yet closed")
    if event['checkAttendance']:
        return response.response_fail(msg="ERROR: attendance needs to be verified")
    attendance = event['attendance']
    event_level = event['engagementLevel']
    level_value = level_to_value_map.get(event_level)
    event_length = event['engagementLengthUnit']
    length_value = length_to_value_map.get(event_length)
    event_length_value = event['engagementLengthValue']
    points_per_skill = length_value * event_length_value * level_value
    skills = event['skills']

    for person in attendance:
        email = person["email"]
        user = User.get_user_from_db(email=email)
        for skill in skills:
            for user_skill in user.skills:
                if user_skill['skill'] == skill:
                    user_skill['value'] += points_per_skill
                    skill_dimensions = list(skill_collection.find_one({"name": skill})['dimensions'])
                    for dimension in skill_dimensions:
                        for user_dimension in user.dimensions:
                            if user_dimension['dimension'] == dimension:
                                user_dimension['value'] += points_per_skill
                                break
            break
        user_collection.update_one({"email": email},
                                   {"$set":
                                    {'skills': user.skills, 'dimensions': user.dimensions}})
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'completed'}})

    return response.response_success()


@events.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = list(event_collection.find({}, {"_id": 0}))
    return response.response_success(objects=all_events)


@events.route('/getAllOpenEvents', methods=['GET'])
def get_all_open_events():
    all_events = list(event_collection.find({"state": "open"}, {"_id": 0}))
    return response.response_success(objects=all_events)


@events.route('/closeEvent/<event_id>/<auth_token>', methods=['POST'])
def close_event(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to close an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'over':
        return response.response_fail(msg="ERROR: Event not over")
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'closed'}})
    return response.response_success()


@events.route('/overEvent/<event_id>/<auth_token>', methods=['POST'])
def over_event(event_id, auth_token):
    user = User.get_user_from_db(token=auth_token)
    if not user.auth_request('faculty'):
        return response.response_fail(msg="ERROR: You do not have permission to set an event to over")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'open':
        return response.response_fail(msg="ERROR: Event not open, cannot be set to over")
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'over'}})
    return response.response_success()
