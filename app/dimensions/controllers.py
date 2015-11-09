from app.database.mongo import dimension_collection
import json
from bson import json_util
from flask import Blueprint

dimensions = Blueprint('dimensions', __name__, url_prefix='/dimensions')


@dimensions.route('/getDimensions', methods=['GET'])
def get_dimensions():
    all_dimensions = dimension_collection.find()
    dimensions_from_db = [json.dumps(e, default=json_util.default) for e in all_dimensions]
    return json.dumps(dimensions_from_db)