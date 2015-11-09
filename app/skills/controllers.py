from app.database.mongo import skill_collection
import json
from bson import json_util
from flask import Blueprint

skills = Blueprint('skills', __name__, url_prefix='/skills')


@skills.route('/getSkills', methods=['GET'])
def get_skills():
    all_skills = skill_collection.find()
    skills_from_db = [json.dumps(e, default=json_util.default) for e in all_skills]
    return json.dumps(skills_from_db)
