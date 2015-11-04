import json
from flask import Flask
from pymongo import MongoClient
from flask import request
from bson import json_util

app = Flask(__name__)

client = MongoClient()
db = client.ActivityTracker
eventCollection = db.Events
studentCollection = db.Students
facultyCollection = db.Faculty
administratorCollection = db.Administrators
skillCollection = db.Skills
dimensionCollection = db.Dimensions

dimensions = []
skills = []
events = []

engagementLevelValues = ["Active", "Passive", "Generative"]
engagementLengthUnits = ["Day", "Week", "Month", "Semester", "Year"]


def get_dimension_names():
    global dimensions
    dimensions = []
    dimensions_list = dimensionCollection.find()
    for dimension in dimensions_list:
        dimensions.append(dimension["name"])


def get_skill_names():
    global skills
    skills = []
    skills_list = skillCollection.find()
    for skill in skills_list:
        skills.append(skill["name"])


def get_event_names():
    global ev ents
    events = []
    events_list = eventCollection.find()
    for event in events_list:
        events.append(event["title"])


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/addSkill', methods=['POST'])
def add_skill():
    data = json.loads(request.data)
    if "name" in data and "dimensions" in data:
        if data["name"] not in skills:
            for d in data["dimensions"]:
                if d not in dimensions:
                    return "Failure"
            mongo_id = skillCollection.insert_one(data).inserted_id
            if mongo_id:
                skills.append(data["name"])
                return "Success"
    return "Failure"


@app.route('/addDimension', methods=['POST'])
def add_dimension():
    data = json.loads(request.data)
    if "name" in data:
        if data["name"] not in dimensions:
            mongo_id = dimensionCollection.insert_one(data).inserted_id
            if mongo_id:
                dimensions.append(data["name"])
                return "Success"
    return "Failure"


@app.route('/addEvent', methods=['POST'])
def add_event():
    data = json.loads(request.data)
    if "title" in data and "format" in data and "topics" in data:
        if data["title"] not in events:
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
                                    mongo_id = eventCollection.insert_one(data).inserted_id
                                    if mongo_id:
                                        events.append(data["title"])
                                        return "Success"
    return json.dumps(data)


@app.route('/getAllEvents', methods=['GET'])
def get_all_events():
    all_events = eventCollection.find()
    events_from_db = [json.dumps(e, default=json_util.default) for e in all_events]
    return json.dumps(events_from_db)

get_dimension_names()
get_event_names()
get_skill_names()
if __name__ == '__main__':
    app.run(debug=True)
