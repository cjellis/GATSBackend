from app.database.db_connection import event_collection, skill_collection, user_collection, dimension_collection
from app.users.user_model import User
from app.utils.msg_tools import ResponseTools as response
import json
from flask import Blueprint, request, render_template
from cerberus import Validator
import datetime
import uuid

###########################################################################
# blueprint for flask
events = Blueprint('events', __name__, url_prefix='/events')

###########################################################################
# Global Constants
length_to_value_map = {
    "1-2": 1,
    "3-4": 2,
    "5-8": 3,
    "9-15": 4,
    "16-29": 5,
    "30-59": 6,
    "60-89": 7,
    "90-119": 8,
    "120-179": 9,
    "180-239": 10,
    "240-299": 11,
    "300-399": 12

}

level_to_value_map = {
    'Active': 1,
    'Passive': 2,
    'Generative': 3
}

###########################################################################
# Validation


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
    if "@neu.edu" not in value:
        error(field, "Email is not an @neu email")

###########################################################################
# Event Schema
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
    'engagementLength': {
        'required': True,
        'type': 'string'
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
        'type': 'string'
    },
    'academicStanding': {
        'type': 'string'
    },
    'major': {
        'type': 'string'
    },
    'residentStatus': {
        'type': 'string',
        'allowed': ['On-Campus', 'Off-Campus', 'Either']
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
    'pointsPerSkill': {
        'type': 'integer'
    },
    'pointsPerDimension': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'dimension': {'type': 'string'},
                'value': {'type': 'integer'}
            }
        }
    },
    'owner': {
        'type': 'string',
        'required': True
    }
}

schemaValidator = Validator(schema)


##########################################################################
# Local Helper Function
def get_points_per_skill(event):
    event_level = event['engagementLevel']
    level_value = level_to_value_map.get(event_level)
    event_length_value = event['engagementLength']
    length_value = length_to_value_map.get(event_length_value)
    return length_value * level_value


def get_points_per_dimension(event):
    all_dimensions = list(dimension_collection.find({}, {"_id": 0}))
    dimension_to_value_map = {}
    for d in all_dimensions:
        dimension_to_value_map[d["name"]] = 0
    points = get_points_per_skill(event)
    for s in event['skills']:
        skill_dimensions = list(skill_collection.find_one({"name": s})['dimensions'])
        for dim in skill_dimensions:
            dimension_to_value_map[dim] += points
    dimension_array = []
    for key, value in dimension_to_value_map.iteritems():
        dimension_array.append({"dimension": key, "value": value})
    return dimension_array

###########################################################################
# API Endpoints


@events.route('/create', methods=['GET'])
@events.route('/create/<email>/<password>', methods=['GET'])
def add(email=None, password=None):
    if email is None or password is None:
        return render_template("login.html")
    else:
        user = User.get_user_if_auth(email=email, password=password)
        if user is None:
                return render_template("failedLogin.html", error="Unknown email/password. Please try again!")
        user = User.get_user_check_auth('faculty', user.token)
        if user is None:
            return render_template("failedLogin.html", error="Unauthorized to create events")
        else:
            all_skills = list(skill_collection.find({}, {"_id": 0}))
            all_skills = sorted(all_skills, key=lambda k: k['name'])
            return render_template('addEvent.html', options=all_skills, auth_token=str(user.token))


@events.route('/successfulAdd', methods=['GET'])
def successfuladd():
    return render_template('successfulAdd.html')


##
# add an event with the post data
# required to pass your authorization token
# adds an id, attendance list, state, and owner to the incoming data
# checks if the user is a faculty user
@events.route('/addEvent/<auth_token>', methods=['POST'])
def add_event(auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to create an event")

    # get the input data and set fields
    data = json.loads(request.data)
    data['id'] = str(uuid.uuid4())
    data['attendance'] = []
    data['state'] = 'open'
    data['owner'] = user.email

    if schemaValidator.validate(data):
        data['pointsPerSkill'] = get_points_per_skill(data)
        data['pointsPerDimension'] = get_points_per_dimension(data)
        mongo_id = event_collection.insert_one(data).inserted_id
        if mongo_id:
            return response.response_success()
        return response.response_fail(msg="ERROR: Could not create event. Please try again")
    return response.response_fail(objects=schemaValidator.errors)


##
# student endpoint to submit attendance to an event
# must pass the event id and the authorization token
# checks that the event is not yet closed or completed
# adds the student to the attendance list for the event
# also adds the event to the students list of events
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


##
# allows faculty to change the event from verify attendance to unverified attendance and vice versa
# authorization token must belong to the faculty owner of the event
@events.route('/changeAttendance/<event_id>/<auth_token>', methods=['POST'])
def change_attendance(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")

    event_collection.update_one({"id": event_id}, {"$set": {"checkAttendance": not event['checkAttendance']}})
    return response.response_success()


##
# allows a faculty owner of an event to get the list of attendees for an event
# list consists of the attendee's first and last name and their email
@events.route('/getAttendance/<event_id>/<auth_token>', methods=['GET'])
def get_attendance(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")

    attendance = event['attendance']

    return response.response_success(objects=attendance)


##
# allows a faculty to owner to distribute points to only those who attended the event
# takes input from the post request which consists of a list of email addresses
# the email addresses are the email addresses of each student that attended
# the state of the event must be closed and the event must be set to verify attendance
@events.route('/verifyAttendance/<event_id>/<auth_token>', methods=['POST'])
def verify_attendance(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'closed':
        return response.response_fail(msg="ERROR: Event not yet closed")
    if not event['checkAttendance']:
        return response.response_fail(msg="ERROR: attendance does not need to be verified")

    points_per_skill = event['pointsPerSkill']
    skills = event['skills']
    points_per_dimension = event["pointsPerDimension"]

    data = json.loads(request.data)
    attendees = data['attendees']
    for email in attendees:
        user = User.get_user_from_db(email=email)
        for skill in skills:
            for user_skill in user.skills:
                if user_skill['skill'] == skill:
                    user_skill['value'] += points_per_skill
                    break
        for dim in points_per_dimension:
            for user_dim in user.dimensions:
                if user_dim['dimension'] == dim["dimension"]:
                    user_dim['value'] += dim["value"]
                    break
        user_collection.update_one({"email": email},
                                   {"$set":
                                    {'skills': user.skills, 'dimensions': user.dimensions}})
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'completed', 'attendance': attendees}})

    return response.response_success()


##
# allows a faculty owner to distribute the points to the student attendees
# it checks that the event is closed and that verify attendance is not set
# it does not take any input from the post body, it simply gives all those
# said they attended the points
@events.route('/distributePoints/<event_id>/<auth_token>', methods=['POST'])
def distribute_points(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to alter an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'closed':
        return response.response_fail(msg="ERROR: Event not yet closed")
    if event['checkAttendance']:
        return response.response_fail(msg="ERROR: attendance needs to be verified")
    attendance = event['attendance']
    points_per_skill = event["pointsPerSkill"]
    skills = event['skills']
    points_per_dimension = event["pointsPerDimension"]

    for person in attendance:
        email = person["email"]
        user = User.get_user_from_db(email=email)
        for skill in skills:
            for user_skill in user.skills:
                if user_skill['skill'] == skill:
                    user_skill['value'] += points_per_skill
                    break
        for dim in points_per_dimension:
            for user_dim in user.dimensions:
                if user_dim['dimension'] == dim["dimension"]:
                    user_dim['value'] += dim["value"]
                    break
        user_collection.update_one({"email": email},
                                   {"$set":
                                    {'skills': user.skills, 'dimensions': user.dimensions}})
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'completed'}})

    return response.response_success()


##
# get all events in the system
@events.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = list(event_collection.find({}, {"_id": 0, "attendance": 0, "owner": 0, "checkAttendance": 0}))
    return response.response_success(objects=all_events)


##
# get all events for a faculty owner
@events.route('/getMyEvents/<auth_token>', methods=['GET'])
def get_my_events(auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        all_events = []
    else:
        all_events = list(event_collection.find({"owner": user.email}, {"_id": 0}))
    return response.response_success(objects=all_events)


##
# gets all open events in the system
@events.route('/getAllOpenEvents', methods=['GET'])
def get_all_open_events():
    all_events = list(event_collection.find({"state": "open"}, {"_id": 0, "attendance": 0, "owner": 0, "checkAttendance": 0}))
    return response.response_success(objects=all_events)


##
# allows a faculty owner to set an event from over to closed
@events.route('/closeEvent/<event_id>/<auth_token>', methods=['POST'])
def close_event(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to close an event")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'over':
        return response.response_fail(msg="ERROR: Event not over")
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'closed'}})
    return response.response_success()


##
# allows a faculty owner to set an event to over
@events.route('/overEvent/<event_id>/<auth_token>', methods=['POST'])
def over_event(event_id, auth_token):
    user = User.get_user_check_auth('faculty', token=auth_token)
    if user is None:
        return response.response_fail(msg="ERROR: You do not have permission to set an event to over")
    event = event_collection.find_one({"id": event_id}, {"_id": 0})
    if event['owner'] != user.email:
        return response.response_fail(msg="ERROR: Not the owner of this event")
    if not event['state'] == 'open':
        return response.response_fail(msg="ERROR: Event not open, cannot be set to over")
    event_collection.update_one({"id": event['id']}, {"$set": {'state': 'over'}})
    return response.response_success()
