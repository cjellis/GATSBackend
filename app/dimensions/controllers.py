from app.database.db_connection import dimension_collection
from flask import Blueprint, jsonify

dimensions = Blueprint('dimensions', __name__, url_prefix='/dimensions')


@dimensions.route('/getDimensions', methods=['GET'])
def get_dimensions():
    all_dimensions = list(dimension_collection.find({}, {"_id": 0}))
    return jsonify({"dimensions": all_dimensions})
