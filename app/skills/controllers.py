from app.database.db_connection import skill_collection
from flask import Blueprint, jsonify

skills = Blueprint('skills', __name__, url_prefix='/skills')


@skills.route('/getSkills', methods=['GET'])
def get_skills():
    all_skills = list(skill_collection.find({}, {"_id": 0}))
    return jsonify({"skills": all_skills})
