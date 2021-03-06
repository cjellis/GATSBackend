from app.database.db_connection import skill_collection
from app.utils.msg_tools import ResponseTools as response
from flask import Blueprint

###########################################################################
# blueprint for flask
skills = Blueprint('skills', __name__, url_prefix='/skills')


###########################################################################
# API Endpoints

##
# get all skills currently in the Mongo DB
@skills.route('/getSkills', methods=['GET'])
def get_skills():
    all_skills = list(skill_collection.find({}, {"_id": 0}))
    return response.response_success(objects=all_skills)
