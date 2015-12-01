from app.database.db_connection import dimension_collection, skill_collection
from app.users.user_model import User
from app.utils.msg_tools import ResponseTools as response
import json
from cerberus import Validator
from flask import Blueprint, request

admin = Blueprint('administrator', __name__, url_prefix='/administrator')


def validate_dimensions_exist(field, value, error):
    for v in value:
        if dimension_collection.find({"name": v}).count() is 0:
            error(field, "Dimension does not exist - " + v)


def validate_skill_name_does_not_exist(field, value, error):
    if skill_collection.find({"name": value}).count() is not 0:
        error(field, "Skill already exists with given name")


def validate_dimension_name_does_not_exist(field, value, error):
    if dimension_collection.find({"name": value}).count() is not 0:
        error(field, "Dimension already exists with given name")

skill_schema = {
    'name': {
        'required': True,
        'type': 'string',
        'validator': validate_skill_name_does_not_exist
    },
    'dimensions': {
        'required': True,
        'type': 'list',
        'schema': {'type': 'string'},
        'validator': validate_dimensions_exist
    }
}

skill_schema_validator = Validator(skill_schema)


dimension_schema = {
    'name': {
        'required': True,
        'type': 'string',
        'validator': validate_dimension_name_does_not_exist
    }
}

dimension_schema_validator = Validator(dimension_schema)


@admin.route('/addSkill/<auth_token>', methods=['POST'])
def add_skill(auth_token):
    if User.get_user_check_auth('admin', token=auth_token) is None:
        return response.response_fail(msg="ERROR: You do not have permission to create a skill")
    data = json.loads(request.data)
    if skill_schema_validator.validate(data):
        mongo_id = skill_collection.insert_one(data).inserted_id
        if mongo_id:
            return response.response_success()
        return response.response_fail(msg="ERROR: Could not create skill. Please try again")
    return response.response_fail(objects=skill_schema_validator.errors)


@admin.route('/addDimension/<auth_token>', methods=['POST'])
def add_dimension(auth_token):
    if User.get_user_check_auth('admin', token=auth_token) is None:
        return response.response_fail(msg="ERROR: You do not have permission to create a dimension")
    data = json.loads(request.data)
    if dimension_schema_validator.validate(data):
        mongo_id = dimension_collection.insert_one(data).inserted_id
        if mongo_id:
            return response.response_success()
        return response.response_fail(msg="ERROR: Could not create dimension. Please try again")
    return response.response_fail(objects=dimension_schema_validator.errors)


