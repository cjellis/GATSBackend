from app.database.mongo import event_collection, skill_collection
import json
from bson import json_util
# Import flask dependencies
from flask import Blueprint, request

# Define the blueprint: 'auth', set its url prefix: app.url/auth
events = Blueprint('events', __name__, url_prefix='/events')

dimensions = []
skills = []
events_list = []

engagementLevelValues = ["Active", "Passive", "Generative"]
engagementLengthUnits = ["Day", "Week", "Month", "Semester", "Year"]


def get_skill_names():
    global skills
    skills = []
    skills_list = skill_collection.find()
    for skill in skills_list:
        skills.append(skill["name"])


def get_event_names():
    global events_list
    events_list = []
    events_list_from_db = event_collection.find()
    for event in events_list_from_db:
        events_list.append(event["title"])


@events.route('/addEvent', methods=['POST'])
def add_event():
    data = json.loads(request.data)
    if "title" in data and "format" in data and "topics" in data:
        if data["title"] not in events_list:
            if "description" in data and "begin" in data and "end" in data:
                if "engagementLengthValue" in data and "engagementLengthUnit" in data:
                    if "recurrence" in data and "location" in data and "sponsoringDepartment" in data:
                        if "pointOfContact" in data and "outcomes" in data and "skills" in data:
                            for s in data["skills"]:
                                if s not in skills:
                                    return json.dumps(data)
                            if "engagementLevel" in data and data["engagementLevel"] in engagementLevelValues:
                                poc = data["pointOfContact"]
                                if "name" in poc and "number" in poc and "email" in poc:
                                    mongo_id = event_collection.insert_one(data).inserted_id
                                    if mongo_id:
                                        events_list.append(data["title"])
                                        return "Success"
    return json.dumps(data)


@events.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = event_collection.find()
    events_from_db = [json.dumps(e, default=json_util.default) for e in all_events]
    return json.dumps(events_from_db)

get_event_names()
get_skill_names()
