from app.database.mongo import dimension_collection, skill_collection
import json
from flask import Blueprint, request

admin = Blueprint('administrator', __name__, url_prefix='/administrator')

dimensions = []
skills = []


def get_skill_names():
    global skills
    skills = []
    skills_list = skill_collection.find()
    for skill in skills_list:
        skills.append(skill["name"])


def get_dimension_names():
    global dimensions
    dimensions = []
    dimensions_list = dimension_collection.find()
    for dimension in dimensions_list:
        dimensions.append(dimension["name"])


@admin.route('/addSkill', methods=['POST'])
def add_skill():
    data = json.loads(request.data)
    if "name" in data and "dimensions" in data:
        if data["name"] not in skills:
            for d in data["dimensions"]:
                if d not in dimensions:
                    return "Failure"
            mongo_id = skill_collection.insert_one(data).inserted_id
            if mongo_id:
                skills.append(data["name"])
                return "Success"
    return "Failure"


@admin.route('/addDimension', methods=['POST'])
def add_dimension():
    data = json.loads(request.data)
    if "name" in data:
        if data["name"] not in dimensions:
            mongo_id = dimension_collection.insert_one(data).inserted_id
            if mongo_id:
                dimensions.append(data["name"])
                return "Success"
    return "Failure"


get_skill_names()
get_dimension_names()

